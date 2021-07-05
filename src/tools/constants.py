import enum

FN_FROM_EXTRACTOR_SPLIT = "_"
FN_FROM_TRANSFORMER_SPLIT = "-"
PCAP_BASE_NAME = "pumarecorder"
NETWORK_RECORDER_POSTROTATE_SCRIPT_NAME = "network_recorder_postrotate.sh"
RAW_FILES_DIR_NAME = "raw"


class Env(enum.Enum):
    DEV_ENV = "PUMA_DEV_ENV"
    STAGING_PATH = "PUMA_ETL_STAGING_PATH"


class DirName(enum.Enum):
    EXTRACTOR_STAGING = "extractor"
    TRANSFORMER_PCAP_STAGING = "transformer_pcap"
    TRANSFORMER_MSGSTORAGE_STAGING = "transformer_msgstorage"
    LOADER_BACKUP = "loader_backup"
    LOADER_ARCHIVER = "loader_archiver"
    MSGSTORAGE = "MsgStorage"


class FileExtension(enum.Enum):
    EXTRACTOR_MSGSTORAGE_REDUNDANT_FILES = "state.backup"
    EXTRACTOR_PCAP_DONE = "done"
    EXTRACTOR_MSGSTORAGE_DONE = "summary.backup"
    TRANSFORMER_DONE = "transformer_done"
    LOADER_BACKUP_DONE = "loader_backup_done"
    TICKS = "ticks"
    QUOTES = "quotes"
    FIN_INSTRUMENTS_LIST = "fin_instruments_list"
    ZST_COMPRESSED = "zst"
    TMP = "tmp"
    PCAP = "pcap"
    TEXT = "txt"


class FIXMsgField(enum.Enum):
    TICK = "35=W"
    QUOTE = "35=X"
    FIN_INSTRUMENT_LIST = "35=y"
