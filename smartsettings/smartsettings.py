from __future__ import annotations
import datetime as dt
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from base64 import b64encode, b64decode

import jsonpickle
from cryptomsg import CryptoMsg


# Timestamp string format
UTC_TIME_STRING_FORMAT = "%Y%m%dT%H%M%S%fZ"


class SmartSettings:
    """The class of smart settings.

    This class can be instantiated directly for settings objects.
    It also can be subclassed for more specific settings classes.

    Equality comparison is defined.
    Indexing operator is defined for accessing the attributes.

    The instance of this class is recursively updatable.
    The left shift operator `<<` is defined for updating attributes from another instance.
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, other: SmartSettings) -> bool:
        if not isinstance(other, type(self)):
            return False
        if len(self.__dict__) != len(other.__dict__):
            return False

        for k in self.__dict__:
            if k not in other.__dict__:
                return False
            if self.__dict__[k] != other.__dict__[k]:
                return False

        return True

    def __getitem__(self, index):
        return getattr(self, index, None)

    def __setitem__(self, index, value):
        setattr(self, index, value)

    def __lshift__(self, other: SmartSettings) -> SmartSettings:
        return self._update_with(other)

    def _update_with(self, other: SmartSettings) -> SmartSettings:
        """Recursively update the attributes with another object of the same type."""
        if not isinstance(other, type(self)):
            raise TypeError(f"{other} is not instance of {type(self)}.")

        for k in other.__dict__:
            if k in self.__dict__:
                if isinstance(self.__dict__[k], SmartSettings):
                    self.__dict__[k]._update_with(other.__dict__[k])
                elif isinstance(self.__dict__[k], list):
                    self._update_list(self.__dict__[k], other.__dict__[k])
                elif isinstance(self.__dict__[k], dict):
                    self._update_dict(self.__dict__[k], other.__dict__[k])
                else:
                    self.__dict__[k] = deepcopy(other.__dict__[k])
            else:
                self.__dict__[k] = deepcopy(other.__dict__[k])

        return self

    def _update_list(self, self_list: list, other_list: list):
        for i in range(len(other_list)):
            if i < len(self_list):
                if isinstance(self_list[i], SmartSettings):
                    self_list[i]._update_with(other_list[i])
                elif isinstance(self_list[i], list):
                    self._update_list(self_list[i], other_list[i])
                elif isinstance(self_list[i], dict):
                    self._update_dict(self_list[i], other_list[i])
                else:
                    self_list[i] = deepcopy(other_list[i])
            else:
                self_list.append(deepcopy(other_list[i]))

    def _update_dict(self, self_dict: dict, other_dict: list):
        for k in other_dict:
            if k in self_dict:
                if isinstance(self_dict[k], SmartSettings):
                    self_dict[k]._update_with(other_dict[k])
                elif isinstance(self_dict[k], list):
                    self._update_list(self_dict[k], other_dict[k])
                elif isinstance(self_dict[k], dict):
                    self._update_dict(self_dict[k], other_dict[k])
                else:
                    self_dict[k] = deepcopy(other_dict[k])
            else:
                self_dict[k] = deepcopy(other_dict[k])


def from_string(
    input_string: str,
    crypto_key: str | None = None,
    **kwargs,
) -> object:
    """Load settings from a string.

    Args:
        input_string: The input string to load settings from.
        crypto_key: The optional decryption key if the string is encrypted.
        kwargs: Other kwargs to `jsonpickle.decode`.

    Returns:
        A settings object.
    """

    if crypto_key is None:
        decrypted_string = input_string
    else:
        h = sha256(crypto_key.encode()).digest()
        key = h[:16]
        iv = h[16:]
        cm = CryptoMsg(key, iv)
        cipher = b64decode(input_string.encode())
        decrypted_string = cm.decrypt_msg(cipher).decode()

    settings = jsonpickle.decode(decrypted_string, **kwargs)
    return settings


def from_file(
    path: Path | str,
    crypto_key: str | None = None,
    default_settings: object = None,
    **kwargs,
) -> object:
    """Load settings from a file.

    Args:
        path: The path of the input file.
        crypto_key: The optional decryption key if the file is encrypted.
        default_settings: The default settings to return if the file does not exist.
        kwargs: Other kwargs to `jsonpickle.decode`.

    Returns:
        A settings object.
    """

    file_path = Path(path)
    if file_path.is_file():
        settings = from_string(
            file_path.read_text(),
            crypto_key=crypto_key,
            **kwargs,
        )
        return settings
    else:
        return deepcopy(default_settings)


def to_string(
    settings,
    crypto_key: str | None = None,
    **kwargs,
) -> str:
    """Store settings to a string.

    Args:
        settings: The settings to be stored.
        crypto_key: The optional encryption key.
        kwargs: Other kwargs to `jsonpickle.encode`.

    Returns:
        A string that represents the settings.
    """

    json_string = jsonpickle.encode(settings, **kwargs)
    if crypto_key is None:
        output_string = json_string
    else:
        h = sha256(crypto_key.encode()).digest()
        key = h[:16]
        iv = h[16:]
        cm = CryptoMsg(key, iv)
        cipher = cm.encrypt_msg(json_string.encode())
        output_string = b64encode(cipher).decode()

    return output_string


def to_file(
    settings,
    path: Path | str,
    crypto_key: str | None = None,
    backup_num: int | None = None,
    **kwargs,
):
    """Store settings to a file.

    Args:
        settings: The settings to be stored.
        path: The path of the output file.
        crypto_key: The optional encryption key.
        backup_num: The number of backup files to keep.
        kwargs: Other kwargs to `jsonpickle.encode`.
    """

    file_path = Path(path)
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        file_path.write_text(to_string(settings, crypto_key=crypto_key, **kwargs))
        return

    if (backup_num is None) or (backup_num > 0):
        extra_text = "_backup_"
        _make_backup_file(file_path, extra_text)
    _delete_backup_files(file_path, backup_num)

    file_path.write_text(to_string(settings, crypto_key=crypto_key, **kwargs))


def _make_backup_file(path: Path | str, extra_text: str = "_"):
    """Make a backup file with timestamp in the same directory."""
    file_path = Path(path)
    backup_path = file_path.with_stem(
        file_path.stem
        + extra_text
        + dt.datetime.now(dt.timezone.utc).strftime(UTC_TIME_STRING_FORMAT)
    )
    backup_path.write_bytes(file_path.read_bytes())


def _delete_backup_files(path: Path | str, backup_num: int | None = None):
    """Leave the newest at most `backup_num` backups and delete others."""
    file_path = Path(path)
    if backup_num is not None:
        parent = file_path.parent
        backup_list = [
            item
            for item in sorted(parent.glob(file_path.stem + "*"))
            if (
                item.is_file()
                and item.suffixes == file_path.suffixes
                and not item.samefile(file_path)
            )
        ]
        delete_list = backup_list[:-backup_num] if backup_num else backup_list
        for item in delete_list:
            item.unlink(missing_ok=True)
