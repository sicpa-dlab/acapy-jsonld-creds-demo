from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.indy_cred_info import IndyCredInfo
from ..models.indy_proof_req_non_revoked import IndyProofReqNonRevoked
from ..types import UNSET, Unset

T = TypeVar("T", bound="IndyCredPrecis")


@attr.s(auto_attribs=True)
class IndyCredPrecis:
    """ """

    cred_def_id: Union[Unset, str] = UNSET
    cred_info: Union[Unset, IndyCredInfo] = UNSET
    cred_rev: Union[Unset, str] = UNSET
    interval: Union[Unset, IndyProofReqNonRevoked] = UNSET
    presentation_referents: Union[Unset, List[str]] = UNSET
    rev_reg_id: Union[Unset, str] = UNSET
    schema_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cred_def_id = self.cred_def_id
        cred_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cred_info, Unset):
            cred_info = self.cred_info.to_dict()

        cred_rev = self.cred_rev
        interval: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.interval, Unset):
            interval = self.interval.to_dict()

        presentation_referents: Union[Unset, List[str]] = UNSET
        if not isinstance(self.presentation_referents, Unset):
            presentation_referents = self.presentation_referents

        rev_reg_id = self.rev_reg_id
        schema_id = self.schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cred_def_id is not UNSET:
            field_dict["cred_def_id"] = cred_def_id
        if cred_info is not UNSET:
            field_dict["cred_info"] = cred_info
        if cred_rev is not UNSET:
            field_dict["cred_rev"] = cred_rev
        if interval is not UNSET:
            field_dict["interval"] = interval
        if presentation_referents is not UNSET:
            field_dict["presentation_referents"] = presentation_referents
        if rev_reg_id is not UNSET:
            field_dict["rev_reg_id"] = rev_reg_id
        if schema_id is not UNSET:
            field_dict["schema_id"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cred_def_id = d.pop("cred_def_id", UNSET)

        _cred_info = d.pop("cred_info", UNSET)
        cred_info: Union[Unset, IndyCredInfo]
        if isinstance(_cred_info, Unset):
            cred_info = UNSET
        else:
            cred_info = IndyCredInfo.from_dict(_cred_info)

        cred_rev = d.pop("cred_rev", UNSET)

        _interval = d.pop("interval", UNSET)
        interval: Union[Unset, IndyProofReqNonRevoked]
        if isinstance(_interval, Unset):
            interval = UNSET
        else:
            interval = IndyProofReqNonRevoked.from_dict(_interval)

        presentation_referents = cast(List[str], d.pop("presentation_referents", UNSET))

        rev_reg_id = d.pop("rev_reg_id", UNSET)

        schema_id = d.pop("schema_id", UNSET)

        indy_cred_precis = cls(
            cred_def_id=cred_def_id,
            cred_info=cred_info,
            cred_rev=cred_rev,
            interval=interval,
            presentation_referents=presentation_referents,
            rev_reg_id=rev_reg_id,
            schema_id=schema_id,
        )

        indy_cred_precis.additional_properties = d
        return indy_cred_precis

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
