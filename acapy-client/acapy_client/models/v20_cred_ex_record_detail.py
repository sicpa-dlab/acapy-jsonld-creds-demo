from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v20_cred_ex_record import V20CredExRecord
from ..models.v20_cred_ex_record_dif import V20CredExRecordDIF
from ..models.v20_cred_ex_record_indy import V20CredExRecordIndy
from ..types import UNSET, Unset

T = TypeVar("T", bound="V20CredExRecordDetail")


@attr.s(auto_attribs=True)
class V20CredExRecordDetail:
    """ """

    cred_ex_record: Union[Unset, V20CredExRecord] = UNSET
    dif: Union[Unset, V20CredExRecordDIF] = UNSET
    indy: Union[Unset, V20CredExRecordIndy] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cred_ex_record: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cred_ex_record, Unset):
            cred_ex_record = self.cred_ex_record.to_dict()

        dif: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dif, Unset):
            dif = self.dif.to_dict()

        indy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.indy, Unset):
            indy = self.indy.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cred_ex_record is not UNSET:
            field_dict["cred_ex_record"] = cred_ex_record
        if dif is not UNSET:
            field_dict["dif"] = dif
        if indy is not UNSET:
            field_dict["indy"] = indy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _cred_ex_record = d.pop("cred_ex_record", UNSET)
        cred_ex_record: Union[Unset, V20CredExRecord]
        if isinstance(_cred_ex_record, Unset):
            cred_ex_record = UNSET
        else:
            cred_ex_record = V20CredExRecord.from_dict(_cred_ex_record)

        _dif = d.pop("dif", UNSET)
        dif: Union[Unset, V20CredExRecordDIF]
        if isinstance(_dif, Unset):
            dif = UNSET
        else:
            dif = V20CredExRecordDIF.from_dict(_dif)

        _indy = d.pop("indy", UNSET)
        indy: Union[Unset, V20CredExRecordIndy]
        if isinstance(_indy, Unset):
            indy = UNSET
        else:
            indy = V20CredExRecordIndy.from_dict(_indy)

        v20_cred_ex_record_detail = cls(
            cred_ex_record=cred_ex_record,
            dif=dif,
            indy=indy,
        )

        v20_cred_ex_record_detail.additional_properties = d
        return v20_cred_ex_record_detail

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
