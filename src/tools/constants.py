from enum import Enum


PCAP_BASE_NAME = "puma-recorder"


class Env(Enum):
    DEV_ENV = "PUMA_DEV_ENV"
    SECRETS_PATH = "PUMA_SECRETS_PATH"
    STAGING_PATH = "PUMA_ETL_STAGING_PATH"


class DirName(Enum):
    EXTRACTOR_STAGING = "extractor"
    TRANSFORMER_PCAP_STAGING = "transformer_pcap"
    TRANSFORMER_MSGSTORAGE_STAGING = "transformer_msgstorage"
    LOADER_BACKUP = "loader_backup"
    LOADER_ARCHIVER = "loader_archiver"
    MSGSTORAGE = "MsgStorage"


class FileExtension(Enum):
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


class FIXMsgField:
    TICK = "35=W"
    QUOTE = "35=X"
    FIN_INSTRUMENT_LIST = "35=y"
