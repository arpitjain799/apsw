#!/usr/bin/env python3

import sys
import pathlib
import gc
import math
import traceback
import os
import glob
import inspect

sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute() / "tools"))

import genfaultinject


def exercise(example_code, expect_exception):
    "This function exercises the code paths where we have fault injection"

    # The module is not imported outside because the init function has
    # several fault injection locations

    import apsw, apsw.ext

    try:
        apsw.config(apsw.SQLITE_CONFIG_URI, 1)
        apsw.config(apsw.SQLITE_CONFIG_MULTITHREAD)
        apsw.config(apsw.SQLITE_CONFIG_PCACHE_HDRSZ)
        apsw.config(apsw.SQLITE_CONFIG_LOG, None)
        apsw.ext.log_sqlite(level=0)
    except apsw.MisuseError:
        pass

    apsw.initialize()
    apsw.log(3, "A message")
    if expect_exception:
        return
    apsw.status(apsw.SQLITE_STATUS_MEMORY_USED)

    for n in """
            SQLITE_VERSION_NUMBER apswversion compile_options keywords memoryused
            sqlite3_sourceid sqlitelibversion using_amalgamation vfsnames
            memoryhighwater
        """.split():
        obj = getattr(apsw, n)
        if callable(obj):
            obj()

    apsw.softheaplimit(100_000_000)
    apsw.hard_heap_limit(100_000_000)
    apsw.randomness(32)
    apsw.enablesharedcache(False)
    apsw.releasememory(1024)
    apsw.exceptionfor(3)
    try:
        apsw.exceptionfor(0xfe)
    except ValueError:
        pass

    for v in ("a'bc", "ab\0c", b"aabbcc", None, math.nan, math.inf, -0.0, -math.inf, 3.1):
        apsw.format_sql_value(v)

    con = apsw.Connection("")
    con.wal_autocheckpoint(1)
    con.execute(
        "pragma page_size=512; pragma auto_vacuum=FULL; pragma journal_mode=wal; create table foo(x)").fetchall()
    with con:
        con.executemany("insert into foo values(zeroblob(1023))", [tuple() for _ in range(500)])

    apsw.zeroblob(77).length()

    con.autovacuum_pages(lambda *args: 1)
    for i in range(20):
        con.wal_autocheckpoint(1)
        victim = con.execute("select rowid from foo order by random() limit 1").fetchall()[0][0]
        con.execute("delete from foo where rowid=?", (victim, ))

    con.config(apsw.SQLITE_DBCONFIG_ENABLE_TRIGGER, 1)
    con.setauthorizer(None)
    con.authorizer = None
    con.collationneeded(None)
    con.collationneeded(lambda *args: 0)
    con.enableloadextension(True)
    con.setbusyhandler(None)
    con.setbusyhandler(lambda *args: True)
    con.createscalarfunction("failme", lambda x: x + 1)
    cur = con.cursor()
    for _ in cur.execute("select failme(3)"):
        cur.description
        cur.description_full
        cur.getdescription()

    if expect_exception:
        return

    apsw.allow_missing_dict_bindings(True)
    con.execute("select :a,:b,$c", {'a': 1, 'c': 3})
    con.execute("select ?, ?, ?, ?", (None, "dsadas", b"xxx", 3.14))
    apsw.allow_missing_dict_bindings(False)

    if expect_exception:
        return

    class Source:

        def Connect(self, *args):
            return "create table ignored(c0, c1, c2, c3)", Source.Table()

        class Table:

            def BestIndexObject(self, iio):
                apsw.ext.index_info_to_dict(iio)
                for n in range(iio.nConstraint):
                    if iio.get_aConstraintUsage_in(n):
                        iio.set_aConstraintUsage_in(n, True)
                        iio.set_aConstraintUsage_argvIndex(n, 1)
                iio.estimatedRows = 7
                return True

            def Open(self):
                return Source.Cursor()

            def UpdateDeleteRow(self, rowid):
                pass

            def UpdateInsertRow(self, rowid, fields):
                return 77

            def UpdateChangeRow(self, rowid, newrowid, fields):
                pass

            def FindFunction(self, name, nargs):
                if nargs == 1:
                    return lambda x: 6
                return [apsw.SQLITE_INDEX_CONSTRAINT_FUNCTION, lambda *args: 7]

        class Cursor:

            def Filter(self, *args):
                self.pos = 0

            def Eof(self):
                return self.pos >= 7

            def Column(self, n):
                return [None, ' ' * n, b"aa" * n, 3.14 * n][n]

            def Next(self):
                self.pos += 1

            def Rowid(self):
                return self.pos

            def Close(self):
                pass

    con.createmodule("vtable", Source(), use_bestindex_object=True, iVersion=3, eponymous=True)
    con.overloadfunction("vtf", 2)
    con.overloadfunction("vtf", 1)
    con.execute("select * from vtable where c2>2 and c1 in (1,2,3)")
    con.execute("create virtual table fred using vtable()")
    con.execute("select vtf(c3) from fred where c3>5; select vtf(c2,c1) from fred where c3>5").fetchall()
    con.execute("delete from fred where c3>5")
    n = 2
    con.execute("insert into fred values(?,?,?,?)", [None, ' ' * n, b"aa" * n, 3.14 * n])
    con.execute("insert into fred(ROWID, c1) values (99, NULL)")
    con.execute("update fred set c2=c3 where rowid=3; update fred set rowid=990 where c2=2")

    def func(*args):
        return 3.14

    con.createscalarfunction("func", func)
    con.execute("select func(1,null,'abc',x'aabb')")

    if expect_exception:
        return

    class SumInt:

        def __init__(self):
            self.v = 0

        def step(self, arg):
            self.v += arg

        def inverse(self, arg):
            self.v -= arg

        def final(self):
            return self.v

        def value(self):
            return self.v

    con.create_window_function("sumint", SumInt)

    for row in con.execute("""
            CREATE TABLE t3(x, y);
            INSERT INTO t3 VALUES('a', 4),
                                ('b', 5),
                                ('c', 3),
                                ('d', 8),
                                ('e', 1);
            -- Use the window function
            SELECT x, sumint(y) OVER (
            ORDER BY x ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
            ) AS sum_y
            FROM t3 ORDER BY x;
        """):
        pass

    for n in """db_names cacheflush changes filename filename_journal
                filename_wal getautocommit in_transaction interrupt last_insert_rowid
                open_flags open_vfs release_memory sqlite3pointer system_errno
                totalchanges txn_state
        """.split():
        obj = getattr(con, n)
        if callable(obj):
            obj()

    con.execute("create table blobby(x); insert into blobby values(?)", (apsw.zeroblob(99), ))
    blob = con.blobopen("main", "blobby", "x", con.last_insert_rowid(), True)
    blob.write(b"hello world")
    blob.seek(80)
    blob.read(10)
    m = bytearray(b"12345678")
    blob.readinto(m)
    blob.tell()
    blob.read(0)
    blob.seek(blob.length())
    blob.read(10)
    blob.seek(0)
    blob.reopen(con.last_insert_rowid())

    blob.close()

    if expect_exception:
        return

    con.cache_stats(True)

    apsw.connection_hooks = [lambda x: None] * 3
    x = apsw.Connection("")
    c = x.cursor()
    try:
        x.backup("main", con, "main")
    except apsw.ThreadingViolationError:
        pass
    del c

    con2 = apsw.Connection("")
    with con2.backup("main", con, "main") as backup:
        backup.step(1)
        backup.remaining
        backup.pagecount
    backup.finish()
    del con2

    con.close()
    del con
    if expect_exception:
        return

    for f in glob.glob("/tmp/dbfile-delme*") + glob.glob("/tmp/myobfudb*"):
        os.remove(f)
    exec(example_code, {"print": lambda *args: None}, None)

    if expect_exception:
        return

    del sys.modules["apsw.ext"]
    gc.collect()
    del apsw


class Tester:

    Proceed = 0x1FACADE
    "magic value keep going (ie do not inject a return value)"

    FAULTT = ZeroDivisionError
    FAULTS = "Fault injection synthesized failure"

    FAULT = FAULTT, FAULTS

    def __init__(self):
        self.returns = genfaultinject.returns
        self.call_remap = {v: k for k, v in genfaultinject.call_map.items()}

        sys.apsw_fault_inject_control = self.fault_inject_control
        sys.apsw_should_fault = lambda *args: False

        lines, start = inspect.getsourcelines(exercise)
        end = start + len(lines)
        self.start_line = start
        self.end_line = end

        with open("example-code.py", "rt") as f:
            code = f.read()
            # we do various transformations but must keep the line numbers the same
            code = code.replace("import os", "import os,contextlib")
            # make it use tmpfs
            code = code.replace('"dbfile"', '"/tmp/dbfile-delme"')
            code = code.replace("myobfudb", "/tmp/myobfudb")
            # logging will fail
            code = code.replace("apsw.ext.log_sqlite()",
                                "with contextlib.suppress(apsw.MisuseError): apsw.ext.log_sqlite(level=0)")
        self.example_code_lines = len(code.split("\n"))
        self.example_code = compile(code, "example-code.py", 'exec')

    @staticmethod
    def apsw_attr(name: str):
        # this is need because we don't do the top level import of apsw
        assert "apsw" in sys.modules
        return getattr(sys.modules["apsw"], name)

    def FaultCall(self, key):
        apsw_attr = self.apsw_attr
        fname = self.call_remap.get(key[0], key[0])
        try:
            if fname in self.returns["pyobject"]:
                self.expect_exception.add(MemoryError)
                raise MemoryError(self.FAULTS)

            if fname == "sqlite3_threadsafe":
                self.expect_exception.add(EnvironmentError)
                return 0

            if fname == "sqlite3_close":
                self.expect_exception.add(apsw_attr("ConnectionNotClosedError"))
                self.expect_exception.add(apsw_attr("IOError"))
                return self.apsw_attr("SQLITE_IOERR")

            if fname == "sqlite3_enable_shared_cache":
                self.expect_exception.add(apsw_attr("Error"))
                return 0xFE  # also does unknown error code to make_exception

            # pointers with 0 being failure
            if fname in {
                    "sqlite3_backup_init", "sqlite3_malloc64", "sqlite3_mprintf", "sqlite3_column_name",
                    "sqlite3_aggregate_context", "sqlite3_expanded_sql"
            }:
                self.expect_exception.add(apsw_attr("SQLError"))
                self.expect_exception.add(MemoryError)
                return 0

            if fname.startswith("sqlite3_"):
                self.expect_exception.add(apsw_attr("TooBigError"))
                return self.apsw_attr("SQLITE_TOOBIG")

            if fname.startswith("PyLong_As"):
                self.expect_exception.add(OverflowError)
                return (-1, OverflowError, self.FAULTS)

            if fname.startswith("Py") or fname in {"_PyBytes_Resize"}:
                # for ones returning -1 on error
                self.expect_exception.add(self.FAULTT)
                return (-1, *self.FAULT)

        finally:
            self.to_fault.pop(key, None)
            self.has_faulted_ever.add(key)
            self.faulted_this_round.append(key)
            if key[2] == "apswvtabFindFunction" or (self.last_key and self.last_key[2] == "apswvtabFindFunction"):
                self.expect_exception.update({TypeError, ValueError})
            self.last_key = key

        print("Unhandled", key)
        breakpoint()

    def fault_inject_control(self, key):
        if self.runplan is not None:
            if not self.runplan:
                return self.Proceed
            elif isinstance(self.runplan, str):
                if key[0] != self.runplan:
                    return self.Proceed
            elif key == self.runplan[0]:
                self.runplan.pop(0)
            else:
                return self.Proceed
        else:
            if self.expect_exception:
                # already have faulted this round
                if key not in self.has_faulted_ever and key not in self.to_fault:
                    self.to_fault[key] = self.faulted_this_round[:]
                return self.Proceed
            if key in self.has_faulted_ever:
                return self.Proceed

        line, percent = self.get_progress()
        if self.runplan is not None:
            print("  Pre" if self.runplan else "Fault", end=" ")
        print(f"faulted: { len(self.has_faulted_ever): 4} / new: { len(self.to_fault): 3}"
              f" cur: { int(percent): 3}%  L{ line } { key }")
        try:
            return self.FaultCall(key)
        finally:
            assert self.expect_exception
            assert key in self.has_faulted_ever

    def exchook(self, e1, e2, e3):
        self.add_exc(e2)

    def add_exc(self, e):
        if e:
            self.last_exc = e
        while e:
            self.exc_happened.append((type(e), e))
            e = e.__context__

    def __enter__(self):
        return self

    def __exit__(self, e1, e2, e3):
        if e2:
            self.add_exc(e2)
        return True  # do not raise

    def get_progress(self):
        # work out what progress in exercise
        ss = traceback.extract_stack()
        curline = self.start_line
        exercise_ok = True
        for frame in ss:
            if frame.filename == __file__ and exercise_ok and frame.name == "exercise":
                curline = max(curline, frame.lineno)
            if frame.filename == "example-code.py":
                if exercise_ok:
                    exercise_ok = False
                    curline = frame.lineno
                curline = max(curline, frame.lineno)

        total_lines = self.end_line - self.start_line + self.example_code_lines
        if exercise_ok:
            curline_pretty = f"{ curline }(exercise)"
            pos = curline - self.start_line
        else:
            curline_pretty = f"{ curline }(example) "
            pos = curline + (self.end_line - self.start_line)

        return curline_pretty, 100 * pos / total_lines

    def verify_exception(self, tested):
        if len(tested) == 0 and len(self.exc_happened) == 0:
            return
        ok = any(e[0] in self.expect_exception for e in self.exc_happened) or any(self.FAULTS in str(e[1])
                                                                                  for e in self.exc_happened)
        # these faults happen in fault handling so can't fault report themselves.
        if tested and list(tested)[0][2] in {"apsw_set_errmsg", "apsw_get_errmsg", "apsw_write_unraisable"}:
            return
        if len(self.exc_happened) < len(tested):
            if any(key[2] == "MakeSqliteMsgFromPyException" for key in tested):
                # we don't report errors in the error handling reporting
                pass
            elif (tested[0][0], tested[1][0]) == ("_PyObject_New", "sqlite3_backup_finish"):
                # backup finish error is ignored because we are handling the
                # object_new error
                pass
            else:
                ok = False
        if not ok:
            print("\nExceptions failed to verify")
            print(f"Got { self.exc_happened }")
            print(f"Expected { self.expect_exception }")
            print(f"Testing { tested }")
            if len(self.exc_happened) < len(tested):
                print("Fewer exceptions observed than faults generated")
            if self.last_exc:
                print("Traceback:")
                tbe = traceback.TracebackException(type(self.last_exc),
                                                   self.last_exc,
                                                   self.last_exc.__traceback__,
                                                   capture_locals=False,
                                                   compact=True)
                for line in tbe.format():
                    print(line)
            sys.exit(1)

    def run(self):
        # keys that we will fault in the future.  we saw these keys while a
        # call had already faulted, so we have to do those same faults again
        # to see this one.  value is list of those previous faults
        self.to_fault = {}
        # keys that have ever faulted across all loops
        self.has_faulted_ever = set()

        self.last_key = None
        use_runplan = False
        last = set(), set()
        complete = False

        sys.excepthook = sys.unraisablehook = self.exchook
        while not complete:
            # exceptions that happened this loop
            self.exc_happened = []
            # exceptions we expected to happen this loop
            self.expect_exception = set()
            # keys we faulted this round
            self.faulted_this_round = []

            if use_runplan:
                if len(self.to_fault) == 0:
                    complete = True
                    self.runplan = "sqlite3_shutdown"
                else:
                    for k, v in self.to_fault.items():
                        self.runplan = v + [k]
                        break
            else:
                self.runplan = None

            self.last_exc = None  # it is ok to see this line when faulting apsw_write_unraisable (comes from PyErr_Print)
            with self:
                try:
                    if complete:
                        # we do this at the very end
                        import apsw
                        apsw.shutdown()
                    else:
                        exercise(self.example_code, self.expect_exception)
                        if not use_runplan and not self.faulted_this_round:
                            use_runplan = True
                            print("\nExercising locations that require multiple failures\n")
                            continue
                finally:
                    gc.collect()

            self.verify_exception(self.faulted_this_round)

            now = set(self.to_fault), set(self.has_faulted_ever)
            if now == last and not complete:
                print("\nUnable to make progress")
                exercise(None)
                break
            else:
                last = now

        if complete:
            print("\nAll faults exercised")

        for n in sorted(self.has_faulted_ever):
            print(n)

        print(f"Total faults: { len(self.has_faulted_ever) }")

        if self.to_fault:
            t = f"Failed to fault { len(self.to_fault) }"
            print("=" * len(t))
            print(t)
            print("=" * len(t))
            for f in sorted(self.to_fault):
                print(f)
            sys.exit(1)

        sys.excepthook = sys.__excepthook__
        sys.unraisablehook = sys.__unraisablehook__


t = Tester()
t.run()
