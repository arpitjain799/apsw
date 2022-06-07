# This file is generated by rst2docstring

from typing import Union, Tuple, List, Optional, Callable, Any, Dict, Iterator, Sequence, Literal, Set

 
SQLITE_VERSION_NUMBER: int
def apswversion() -> str: ...
compile_options: Tuple
def complete(statement: str) -> bool: ...
def config(op: int, *args) -> None: ...
connection_hooks: List[Callable]
def enablesharedcache(enable: bool) -> None: ...
def exceptionfor(code: int) -> Exception: ...
def fork_checker() -> None: ...
def format_sql_value(value: Union[None, int, float, bytes, str]) -> str: ...
def initialize() -> None: ...
keywords: Set[str]
def log(errorcode: int, message: str) -> None: ...
def main(): ...
def memoryhighwater(reset: bool = False) -> int: ...
def memoryused() -> int: ...
def randomness(amount: int)  -> bytes: ...
def releasememory(amount: int) -> int: ...
def shutdown() -> None: ...
def softheaplimit(limit: int) -> int: ...
def sqlite3_sourceid() -> str: ...
def sqlitelibversion() -> str: ...
def status(op: int, reset: bool = False) -> Tuple[int, int]: ...
using_amalgamation: bool
def vfsnames() -> List[str]: ...

class Backup:
    def __init__(self): ...
    def close(self, force: bool = False) -> None: ...
    done: bool
    def __enter__(self) -> Backup: ...
    def __exit__(self) -> Literal[False]: ...
    def finish(self) -> None: ...
    pagecount: int
    remaining: int
    def step(self, npages: int = -1) -> bool: ...

class Blob:
    def __init__(self): ...
    def close(self, force: bool = False) -> None: ...
    def __enter__(self) -> Blob: ...
    def __exit__(self) -> Literal[False]: ...
    def length(self) -> int: ...
    def read(self, length: int = -1) -> bytes: ...
    def readinto(self, buffer, offset: int = 0, length: int = -1) -> None: ...
    def reopen(self, rowid: int) -> None: ...
    def seek(self, offset: int, whence: int = 0) -> None: ...
    def tell(self) -> int: ...
    def write(self, data: bytes) -> None: ...

class Connection:
    def __init__(self, filename: str, flags: int = SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE, vfs: Optional[str] = None, statementcachesize: int = 100): ...
    def autovacuum_pages(self, callable: Optional[Callable]) -> None: ...
    def backup(self, databasename: str, sourceconnection: Connection, sourcedatabasename: str)  -> Backup: ...
    def blobopen(self, database: str, table: str, column: str, rowid: int, writeable: bool)  -> Blob: ...
    def changes(self) -> int: ...
    def close(self, force: bool = False): ...
    def collationneeded(self, callable: Optional[Callable]) -> None: ...
    def config(self, op: int, *args) -> int: ...
    def createaggregatefunction(self, name: str, factory: Optional[Callable], numargs: int = -1): ...
    def createcollation(self, name: str, callback: Optional[Callable]) -> None: ...
    def createmodule(self, name: str, datasource: Any) -> None: ...
    def createscalarfunction(self, name: str, callable: Optional[Callable], numargs: int = -1, deterministic: bool = False) -> None: ...
    def cursor(self) -> Cursor: ...
    def db_filename(self, name: str) -> str: ...
    def deserialize(self, name: str, contents: bytes) -> None: ...
    def enableloadextension(self, enable: bool) -> None: ...
    def __enter__(self) -> Connection: ...
    def __exit__(self) -> Literal[False]: ...
    def filecontrol(self, dbname: str, op: int, pointer: int) -> bool: ...
    filename: str
    def getautocommit(self) -> bool: ...
    def getexectrace(self) -> Optional[Callable]: ...
    def getrowtrace(self) -> Optional[Callable]: ...
    def interrupt(self) -> None: ...
    def last_insert_rowid(self) -> int: ...
    def limit(self, id: int, newval: int = -1) -> int: ...
    def loadextension(self, filename: str, entrypoint: str = None) -> None: ...
    open_flags: int
    open_vfs: str
    def overloadfunction(self, name: str, nargs: int) -> None: ...
    def readonly(self, name: str) -> bool: ...
    def serialize(self, name: str) -> bytes: ...
    def set_last_insert_rowid(self, rowid: int) -> None: ...
    def setauthorizer(self, callable: Optional[Callable]) -> None: ...
    def setbusyhandler(self, callable: Optional[Callable]) -> None: ...
    def setbusytimeout(self, milliseconds: int) -> None: ...
    def setcommithook(self, callable: Optional[Callable]) -> None: ...
    def setexectrace(self, callable: Optional[Callable]) -> None: ...
    def setprofile(self, callable: Optional[Callable]) -> None: ...
    def setprogresshandler(self, callable: Optional[Callable], nsteps: int = 20): ...
    def setrollbackhook(self, callable: Optional[Callable]) -> None: ...
    def setrowtrace(self, callable: Optional[Callable]) -> None: ...
    def setupdatehook(self, callable: Optional[Callable]) -> None: ...
    def setwalhook(self, callable: Optional[Callable]) -> None: ...
    def sqlite3pointer(self) -> int: ...
    def status(self, op: int, reset: bool = False) -> Tuple[int, int]: ...
    def totalchanges(self) -> int: ...
    def txn_state(self, schema: str = None) -> int: ...
    def wal_autocheckpoint(self, n: int) -> None: ...
    def wal_checkpoint(self, dbname: Optional[str] = None, mode: int = SQLITE_CHECKPOINT_PASSIVE) -> Tuple[int, int]: ...

class Cursor:
    def __init__(self): ...
    def close(self, force: bool = False) -> None: ...
    description: tuple
    def execute(self, statements: str, bindings: Optional[Union[Sequence,Dict]] = None) -> Cursor: ...
    def executemany(self, statements: str, sequenceofbindings: Sequence[Union[Sequence,Dict]]) -> Cursor: ...
    def fetchall(self) -> list: ...
    def fetchone(self) -> Optional[Any]: ...
    def getconnection(self) -> Connection: ...
    def getdescription(self) -> tuple: ...
    def getexectrace(self) -> Optional[Callable]: ...
    def getrowtrace(self) -> Optional[Callable]: ...
    def setexectrace(self, callable: Optional[Callable]) -> None: ...
    def setrowtrace(self, callable: Optional[Callable]) -> None: ...

class URIFilename:
    def __init__(self): ...
    def filename(self) -> str: ...
    def uri_boolean(self, name: str, default: bool) -> bool: ...
    def uri_int(self, name: str, default: int) -> int: ...
    def uri_parameter(self, name: str) -> Optional[str]: ...

class VFSFile:
    def __init__(self, vfs: str, filename: Union[str,URIFilename], flags: List[int]): ...
    def excepthook(self, etype, evalue, etraceback): ...
    def xCheckReservedLock(self) -> bool: ...
    def xClose(self) -> None: ...
    def xDeviceCharacteristics(self) -> int: ...
    def xFileControl(self, op: int, ptr: int) -> bool: ...
    def xFileSize(self) -> int: ...
    def xLock(self, level: int) -> None: ...
    def xRead(self, amount: int, offset: int) -> bytes: ...
    def xSectorSize(self) -> int: ...
    def xSync(self, flags: int) -> None: ...
    def xTruncate(self, newsize: int) -> None: ...
    def xUnlock(self, level: int) -> None: ...
    def xWrite(self, data: bytes, offset: int) -> None: ...

class VFS:
    def __init__(self, name: str, base: str = None, makedefault: bool = False, maxpathname: int = 1024): ...
    def excepthook(self, *args) -> Any: ...
    def unregister(self) -> None: ...
    def xAccess(self, pathname: str, flags: int) -> bool: ...
    def xCurrentTime(self)  -> float: ...
    def xDelete(self, filename: str, syncdir: bool) -> None: ...
    def xDlClose(self, handle: int) -> None: ...
    def xDlError(self) -> str: ...
    def xDlOpen(self, filename: str) -> int: ...
    def xDlSym(self, handle: int, symbol: str) -> int: ...
    def xFullPathname(self, name: str) -> str: ...
    def xGetLastError(self) -> Tuple[int, str]: ...
    def xGetSystemCall(self, name: str) -> Optional[int]: ...
    def xNextSystemCall(self, name: Optional[str]) -> Optional[str]: ...
    def xOpen(self, name: Optional[Union[str,URIFilename]], flags: List[int]) -> VFSFile: ...
    def xRandomness(self, numbytes: int) -> bytes: ...
    def xSetSystemCall(self, name: Optional[str], pointer: int) -> bool: ...
    def xSleep(self, microseconds: int) -> int: ...

class zeroblob:
    def __init__(self, size: int): ...
    def length(self) -> int: ...


SQLITE_ABORT: int
SQLITE_ABORT_ROLLBACK: int
SQLITE_ACCESS_EXISTS: int
SQLITE_ACCESS_READ: int
SQLITE_ACCESS_READWRITE: int
SQLITE_ALTER_TABLE: int
SQLITE_ANALYZE: int
SQLITE_ATTACH: int
SQLITE_AUTH: int
SQLITE_AUTH_USER: int
SQLITE_BUSY: int
SQLITE_BUSY_RECOVERY: int
SQLITE_BUSY_SNAPSHOT: int
SQLITE_BUSY_TIMEOUT: int
SQLITE_CANTOPEN: int
SQLITE_CANTOPEN_CONVPATH: int
SQLITE_CANTOPEN_DIRTYWAL: int
SQLITE_CANTOPEN_FULLPATH: int
SQLITE_CANTOPEN_ISDIR: int
SQLITE_CANTOPEN_NOTEMPDIR: int
SQLITE_CANTOPEN_SYMLINK: int
SQLITE_CHECKPOINT_FULL: int
SQLITE_CHECKPOINT_PASSIVE: int
SQLITE_CHECKPOINT_RESTART: int
SQLITE_CHECKPOINT_TRUNCATE: int
SQLITE_CONFIG_COVERING_INDEX_SCAN: int
SQLITE_CONFIG_GETMALLOC: int
SQLITE_CONFIG_GETMUTEX: int
SQLITE_CONFIG_GETPCACHE: int
SQLITE_CONFIG_GETPCACHE2: int
SQLITE_CONFIG_HEAP: int
SQLITE_CONFIG_LOG: int
SQLITE_CONFIG_LOOKASIDE: int
SQLITE_CONFIG_MALLOC: int
SQLITE_CONFIG_MEMDB_MAXSIZE: int
SQLITE_CONFIG_MEMSTATUS: int
SQLITE_CONFIG_MMAP_SIZE: int
SQLITE_CONFIG_MULTITHREAD: int
SQLITE_CONFIG_MUTEX: int
SQLITE_CONFIG_PAGECACHE: int
SQLITE_CONFIG_PCACHE: int
SQLITE_CONFIG_PCACHE2: int
SQLITE_CONFIG_PCACHE_HDRSZ: int
SQLITE_CONFIG_PMASZ: int
SQLITE_CONFIG_SCRATCH: int
SQLITE_CONFIG_SERIALIZED: int
SQLITE_CONFIG_SINGLETHREAD: int
SQLITE_CONFIG_SMALL_MALLOC: int
SQLITE_CONFIG_SORTERREF_SIZE: int
SQLITE_CONFIG_SQLLOG: int
SQLITE_CONFIG_STMTJRNL_SPILL: int
SQLITE_CONFIG_URI: int
SQLITE_CONFIG_WIN32_HEAPSIZE: int
SQLITE_CONSTRAINT: int
SQLITE_CONSTRAINT_CHECK: int
SQLITE_CONSTRAINT_COMMITHOOK: int
SQLITE_CONSTRAINT_DATATYPE: int
SQLITE_CONSTRAINT_FOREIGNKEY: int
SQLITE_CONSTRAINT_FUNCTION: int
SQLITE_CONSTRAINT_NOTNULL: int
SQLITE_CONSTRAINT_PINNED: int
SQLITE_CONSTRAINT_PRIMARYKEY: int
SQLITE_CONSTRAINT_ROWID: int
SQLITE_CONSTRAINT_TRIGGER: int
SQLITE_CONSTRAINT_UNIQUE: int
SQLITE_CONSTRAINT_VTAB: int
SQLITE_COPY: int
SQLITE_CORRUPT: int
SQLITE_CORRUPT_INDEX: int
SQLITE_CORRUPT_SEQUENCE: int
SQLITE_CORRUPT_VTAB: int
SQLITE_CREATE_INDEX: int
SQLITE_CREATE_TABLE: int
SQLITE_CREATE_TEMP_INDEX: int
SQLITE_CREATE_TEMP_TABLE: int
SQLITE_CREATE_TEMP_TRIGGER: int
SQLITE_CREATE_TEMP_VIEW: int
SQLITE_CREATE_TRIGGER: int
SQLITE_CREATE_VIEW: int
SQLITE_CREATE_VTABLE: int
SQLITE_DBCONFIG_DEFENSIVE: int
SQLITE_DBCONFIG_DQS_DDL: int
SQLITE_DBCONFIG_DQS_DML: int
SQLITE_DBCONFIG_ENABLE_FKEY: int
SQLITE_DBCONFIG_ENABLE_FTS3_TOKENIZER: int
SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION: int
SQLITE_DBCONFIG_ENABLE_QPSG: int
SQLITE_DBCONFIG_ENABLE_TRIGGER: int
SQLITE_DBCONFIG_ENABLE_VIEW: int
SQLITE_DBCONFIG_LEGACY_ALTER_TABLE: int
SQLITE_DBCONFIG_LEGACY_FILE_FORMAT: int
SQLITE_DBCONFIG_LOOKASIDE: int
SQLITE_DBCONFIG_MAINDBNAME: int
SQLITE_DBCONFIG_MAX: int
SQLITE_DBCONFIG_NO_CKPT_ON_CLOSE: int
SQLITE_DBCONFIG_RESET_DATABASE: int
SQLITE_DBCONFIG_TRIGGER_EQP: int
SQLITE_DBCONFIG_TRUSTED_SCHEMA: int
SQLITE_DBCONFIG_WRITABLE_SCHEMA: int
SQLITE_DBSTATUS_CACHE_HIT: int
SQLITE_DBSTATUS_CACHE_MISS: int
SQLITE_DBSTATUS_CACHE_SPILL: int
SQLITE_DBSTATUS_CACHE_USED: int
SQLITE_DBSTATUS_CACHE_USED_SHARED: int
SQLITE_DBSTATUS_CACHE_WRITE: int
SQLITE_DBSTATUS_DEFERRED_FKS: int
SQLITE_DBSTATUS_LOOKASIDE_HIT: int
SQLITE_DBSTATUS_LOOKASIDE_MISS_FULL: int
SQLITE_DBSTATUS_LOOKASIDE_MISS_SIZE: int
SQLITE_DBSTATUS_LOOKASIDE_USED: int
SQLITE_DBSTATUS_MAX: int
SQLITE_DBSTATUS_SCHEMA_USED: int
SQLITE_DBSTATUS_STMT_USED: int
SQLITE_DELETE: int
SQLITE_DENY: int
SQLITE_DETACH: int
SQLITE_DONE: int
SQLITE_DROP_INDEX: int
SQLITE_DROP_TABLE: int
SQLITE_DROP_TEMP_INDEX: int
SQLITE_DROP_TEMP_TABLE: int
SQLITE_DROP_TEMP_TRIGGER: int
SQLITE_DROP_TEMP_VIEW: int
SQLITE_DROP_TRIGGER: int
SQLITE_DROP_VIEW: int
SQLITE_DROP_VTABLE: int
SQLITE_EMPTY: int
SQLITE_ERROR: int
SQLITE_ERROR_MISSING_COLLSEQ: int
SQLITE_ERROR_RETRY: int
SQLITE_ERROR_SNAPSHOT: int
SQLITE_FAIL: int
SQLITE_FCNTL_BEGIN_ATOMIC_WRITE: int
SQLITE_FCNTL_BUSYHANDLER: int
SQLITE_FCNTL_CHUNK_SIZE: int
SQLITE_FCNTL_CKPT_DONE: int
SQLITE_FCNTL_CKPT_START: int
SQLITE_FCNTL_CKSM_FILE: int
SQLITE_FCNTL_COMMIT_ATOMIC_WRITE: int
SQLITE_FCNTL_COMMIT_PHASETWO: int
SQLITE_FCNTL_DATA_VERSION: int
SQLITE_FCNTL_EXTERNAL_READER: int
SQLITE_FCNTL_FILE_POINTER: int
SQLITE_FCNTL_GET_LOCKPROXYFILE: int
SQLITE_FCNTL_HAS_MOVED: int
SQLITE_FCNTL_JOURNAL_POINTER: int
SQLITE_FCNTL_LAST_ERRNO: int
SQLITE_FCNTL_LOCKSTATE: int
SQLITE_FCNTL_LOCK_TIMEOUT: int
SQLITE_FCNTL_MMAP_SIZE: int
SQLITE_FCNTL_OVERWRITE: int
SQLITE_FCNTL_PDB: int
SQLITE_FCNTL_PERSIST_WAL: int
SQLITE_FCNTL_POWERSAFE_OVERWRITE: int
SQLITE_FCNTL_PRAGMA: int
SQLITE_FCNTL_RBU: int
SQLITE_FCNTL_RESERVE_BYTES: int
SQLITE_FCNTL_ROLLBACK_ATOMIC_WRITE: int
SQLITE_FCNTL_SET_LOCKPROXYFILE: int
SQLITE_FCNTL_SIZE_HINT: int
SQLITE_FCNTL_SIZE_LIMIT: int
SQLITE_FCNTL_SYNC: int
SQLITE_FCNTL_SYNC_OMITTED: int
SQLITE_FCNTL_TEMPFILENAME: int
SQLITE_FCNTL_TRACE: int
SQLITE_FCNTL_VFSNAME: int
SQLITE_FCNTL_VFS_POINTER: int
SQLITE_FCNTL_WAL_BLOCK: int
SQLITE_FCNTL_WIN32_AV_RETRY: int
SQLITE_FCNTL_WIN32_GET_HANDLE: int
SQLITE_FCNTL_WIN32_SET_HANDLE: int
SQLITE_FCNTL_ZIPVFS: int
SQLITE_FORMAT: int
SQLITE_FULL: int
SQLITE_FUNCTION: int
SQLITE_IGNORE: int
SQLITE_INDEX_CONSTRAINT_EQ: int
SQLITE_INDEX_CONSTRAINT_FUNCTION: int
SQLITE_INDEX_CONSTRAINT_GE: int
SQLITE_INDEX_CONSTRAINT_GLOB: int
SQLITE_INDEX_CONSTRAINT_GT: int
SQLITE_INDEX_CONSTRAINT_IS: int
SQLITE_INDEX_CONSTRAINT_ISNOT: int
SQLITE_INDEX_CONSTRAINT_ISNOTNULL: int
SQLITE_INDEX_CONSTRAINT_ISNULL: int
SQLITE_INDEX_CONSTRAINT_LE: int
SQLITE_INDEX_CONSTRAINT_LIKE: int
SQLITE_INDEX_CONSTRAINT_LIMIT: int
SQLITE_INDEX_CONSTRAINT_LT: int
SQLITE_INDEX_CONSTRAINT_MATCH: int
SQLITE_INDEX_CONSTRAINT_NE: int
SQLITE_INDEX_CONSTRAINT_OFFSET: int
SQLITE_INDEX_CONSTRAINT_REGEXP: int
SQLITE_INDEX_SCAN_UNIQUE: int
SQLITE_INSERT: int
SQLITE_INTERNAL: int
SQLITE_INTERRUPT: int
SQLITE_IOCAP_ATOMIC: int
SQLITE_IOCAP_ATOMIC16K: int
SQLITE_IOCAP_ATOMIC1K: int
SQLITE_IOCAP_ATOMIC2K: int
SQLITE_IOCAP_ATOMIC32K: int
SQLITE_IOCAP_ATOMIC4K: int
SQLITE_IOCAP_ATOMIC512: int
SQLITE_IOCAP_ATOMIC64K: int
SQLITE_IOCAP_ATOMIC8K: int
SQLITE_IOCAP_BATCH_ATOMIC: int
SQLITE_IOCAP_IMMUTABLE: int
SQLITE_IOCAP_POWERSAFE_OVERWRITE: int
SQLITE_IOCAP_SAFE_APPEND: int
SQLITE_IOCAP_SEQUENTIAL: int
SQLITE_IOCAP_UNDELETABLE_WHEN_OPEN: int
SQLITE_IOERR: int
SQLITE_IOERR_ACCESS: int
SQLITE_IOERR_AUTH: int
SQLITE_IOERR_BEGIN_ATOMIC: int
SQLITE_IOERR_BLOCKED: int
SQLITE_IOERR_CHECKRESERVEDLOCK: int
SQLITE_IOERR_CLOSE: int
SQLITE_IOERR_COMMIT_ATOMIC: int
SQLITE_IOERR_CONVPATH: int
SQLITE_IOERR_CORRUPTFS: int
SQLITE_IOERR_DATA: int
SQLITE_IOERR_DELETE: int
SQLITE_IOERR_DELETE_NOENT: int
SQLITE_IOERR_DIR_CLOSE: int
SQLITE_IOERR_DIR_FSYNC: int
SQLITE_IOERR_FSTAT: int
SQLITE_IOERR_FSYNC: int
SQLITE_IOERR_GETTEMPPATH: int
SQLITE_IOERR_LOCK: int
SQLITE_IOERR_MMAP: int
SQLITE_IOERR_NOMEM: int
SQLITE_IOERR_RDLOCK: int
SQLITE_IOERR_READ: int
SQLITE_IOERR_ROLLBACK_ATOMIC: int
SQLITE_IOERR_SEEK: int
SQLITE_IOERR_SHMLOCK: int
SQLITE_IOERR_SHMMAP: int
SQLITE_IOERR_SHMOPEN: int
SQLITE_IOERR_SHMSIZE: int
SQLITE_IOERR_SHORT_READ: int
SQLITE_IOERR_TRUNCATE: int
SQLITE_IOERR_UNLOCK: int
SQLITE_IOERR_VNODE: int
SQLITE_IOERR_WRITE: int
SQLITE_LIMIT_ATTACHED: int
SQLITE_LIMIT_COLUMN: int
SQLITE_LIMIT_COMPOUND_SELECT: int
SQLITE_LIMIT_EXPR_DEPTH: int
SQLITE_LIMIT_FUNCTION_ARG: int
SQLITE_LIMIT_LENGTH: int
SQLITE_LIMIT_LIKE_PATTERN_LENGTH: int
SQLITE_LIMIT_SQL_LENGTH: int
SQLITE_LIMIT_TRIGGER_DEPTH: int
SQLITE_LIMIT_VARIABLE_NUMBER: int
SQLITE_LIMIT_VDBE_OP: int
SQLITE_LIMIT_WORKER_THREADS: int
SQLITE_LOCKED: int
SQLITE_LOCKED_SHAREDCACHE: int
SQLITE_LOCKED_VTAB: int
SQLITE_LOCK_EXCLUSIVE: int
SQLITE_LOCK_NONE: int
SQLITE_LOCK_PENDING: int
SQLITE_LOCK_RESERVED: int
SQLITE_LOCK_SHARED: int
SQLITE_MISMATCH: int
SQLITE_MISUSE: int
SQLITE_NOLFS: int
SQLITE_NOMEM: int
SQLITE_NOTADB: int
SQLITE_NOTFOUND: int
SQLITE_NOTICE: int
SQLITE_NOTICE_RECOVER_ROLLBACK: int
SQLITE_NOTICE_RECOVER_WAL: int
SQLITE_OK: int
SQLITE_OK_LOAD_PERMANENTLY: int
SQLITE_OK_SYMLINK: int
SQLITE_OPEN_AUTOPROXY: int
SQLITE_OPEN_CREATE: int
SQLITE_OPEN_DELETEONCLOSE: int
SQLITE_OPEN_EXCLUSIVE: int
SQLITE_OPEN_EXRESCODE: int
SQLITE_OPEN_FULLMUTEX: int
SQLITE_OPEN_MAIN_DB: int
SQLITE_OPEN_MAIN_JOURNAL: int
SQLITE_OPEN_MEMORY: int
SQLITE_OPEN_NOFOLLOW: int
SQLITE_OPEN_NOMUTEX: int
SQLITE_OPEN_PRIVATECACHE: int
SQLITE_OPEN_READONLY: int
SQLITE_OPEN_READWRITE: int
SQLITE_OPEN_SHAREDCACHE: int
SQLITE_OPEN_SUBJOURNAL: int
SQLITE_OPEN_SUPER_JOURNAL: int
SQLITE_OPEN_TEMP_DB: int
SQLITE_OPEN_TEMP_JOURNAL: int
SQLITE_OPEN_TRANSIENT_DB: int
SQLITE_OPEN_URI: int
SQLITE_OPEN_WAL: int
SQLITE_PERM: int
SQLITE_PRAGMA: int
SQLITE_PROTOCOL: int
SQLITE_RANGE: int
SQLITE_READ: int
SQLITE_READONLY: int
SQLITE_READONLY_CANTINIT: int
SQLITE_READONLY_CANTLOCK: int
SQLITE_READONLY_DBMOVED: int
SQLITE_READONLY_DIRECTORY: int
SQLITE_READONLY_RECOVERY: int
SQLITE_READONLY_ROLLBACK: int
SQLITE_RECURSIVE: int
SQLITE_REINDEX: int
SQLITE_REPLACE: int
SQLITE_ROLLBACK: int
SQLITE_ROW: int
SQLITE_SAVEPOINT: int
SQLITE_SCHEMA: int
SQLITE_SELECT: int
SQLITE_SHM_EXCLUSIVE: int
SQLITE_SHM_LOCK: int
SQLITE_SHM_SHARED: int
SQLITE_SHM_UNLOCK: int
SQLITE_STATUS_MALLOC_COUNT: int
SQLITE_STATUS_MALLOC_SIZE: int
SQLITE_STATUS_MEMORY_USED: int
SQLITE_STATUS_PAGECACHE_OVERFLOW: int
SQLITE_STATUS_PAGECACHE_SIZE: int
SQLITE_STATUS_PAGECACHE_USED: int
SQLITE_STATUS_PARSER_STACK: int
SQLITE_STATUS_SCRATCH_OVERFLOW: int
SQLITE_STATUS_SCRATCH_SIZE: int
SQLITE_STATUS_SCRATCH_USED: int
SQLITE_SYNC_DATAONLY: int
SQLITE_SYNC_FULL: int
SQLITE_SYNC_NORMAL: int
SQLITE_TOOBIG: int
SQLITE_TRANSACTION: int
SQLITE_TXN_NONE: int
SQLITE_TXN_READ: int
SQLITE_TXN_WRITE: int
SQLITE_UPDATE: int
SQLITE_VTAB_CONSTRAINT_SUPPORT: int
SQLITE_VTAB_DIRECTONLY: int
SQLITE_VTAB_INNOCUOUS: int
SQLITE_WARNING: int
SQLITE_WARNING_AUTOINDEX: int


mapping_access: Dict[Union[str,int],Union[int,str]]
mapping_authorizer_function: Dict[Union[str,int],Union[int,str]]
mapping_authorizer_return: Dict[Union[str,int],Union[int,str]]
mapping_bestindex_constraints: Dict[Union[str,int],Union[int,str]]
mapping_config: Dict[Union[str,int],Union[int,str]]
mapping_conflict_resolution_modes: Dict[Union[str,int],Union[int,str]]
mapping_db_config: Dict[Union[str,int],Union[int,str]]
mapping_db_status: Dict[Union[str,int],Union[int,str]]
mapping_device_characteristics: Dict[Union[str,int],Union[int,str]]
mapping_extended_result_codes: Dict[Union[str,int],Union[int,str]]
mapping_file_control: Dict[Union[str,int],Union[int,str]]
mapping_limits: Dict[Union[str,int],Union[int,str]]
mapping_locking_level: Dict[Union[str,int],Union[int,str]]
mapping_open_flags: Dict[Union[str,int],Union[int,str]]
mapping_result_codes: Dict[Union[str,int],Union[int,str]]
mapping_status: Dict[Union[str,int],Union[int,str]]
mapping_sync: Dict[Union[str,int],Union[int,str]]
mapping_txn_state: Dict[Union[str,int],Union[int,str]]
mapping_virtual_table_configuration_options: Dict[Union[str,int],Union[int,str]]
mapping_virtual_table_scan_flags: Dict[Union[str,int],Union[int,str]]
mapping_wal_checkpoint: Dict[Union[str,int],Union[int,str]]
mapping_xshmlock_flags: Dict[Union[str,int],Union[int,str]]


class Error(Exception): ...
class AbortError(Error): ...
class AuthError(Error): ...
class BindingsError(Error): ...
class BusyError(Error): ...
class CantOpenError(Error): ...
class ConnectionClosedError(Error): ...
class ConnectionNotClosedError(Error): ...
class ConstraintError(Error): ...
class CorruptError(Error): ...
class CursorClosedError(Error): ...
class EmptyError(Error): ...
class ExecTraceAbort(Error): ...
class ExecutionCompleteError(Error): ...
class ExtensionLoadingError(Error): ...
class ForkingViolationError(Error): ...
class FormatError(Error): ...
class FullError(Error): ...
class IOError(Error): ...
class IncompleteExecutionError(Error): ...
class InternalError(Error): ...
class InterruptError(Error): ...
class LockedError(Error): ...
class MismatchError(Error): ...
class MisuseError(Error): ...
class NoLFSError(Error): ...
class NoMemError(Error): ...
class NotADBError(Error): ...
class NotFoundError(Error): ...
class PermissionsError(Error): ...
class ProtocolError(Error): ...
class RangeError(Error): ...
class ReadOnlyError(Error): ...
class SQLError(Error): ...
class SchemaChangeError(Error): ...
class ThreadingViolationError(Error): ...
class TooBigError(Error): ...
class VFSFileClosedError(Error): ...
class VFSNotImplementedError(Error): ...
