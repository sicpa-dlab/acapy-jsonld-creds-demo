from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v20_cred_filter import V20CredFilter
from ..models.v20_cred_preview import V20CredPreview
from ..types import UNSET, Unset

T = TypeVar("T", bound="V20CredOfferRequest")


@attr.s(auto_attribs=True)
class V20CredOfferRequest:
    """ """

    connection_id: str
    credential_preview: V20CredPreview
    filter_: V20CredFilter
    auto_issue: Union[Unset, bool] = UNSET
    auto_remove: Union[Unset, bool] = UNSET
    comment: Union[Unset, None, str] = UNSET
    trace: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connection_id = self.connection_id
        credential_preview = self.credential_preview.to_dict()

        filter_ = self.filter_.to_dict()

        auto_issue = self.auto_issue
        auto_remove = self.auto_remove
        comment = self.comment
        trace = self.trace

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connection_id": connection_id,
                "credential_preview": credential_preview,
                "filter": filter_,
            }
        )
        if auto_issue is not UNSET:
            field_dict["auto_issue"] = auto_issue
        if auto_remove is not UNSET:
            field_dict["auto_remove"] = auto_remove
        if comment is not UNSET:
            field_dict["comment"] = comment
        if trace is not UNSET:
            field_dict["trace"] = trace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        connection_id = d.pop("connection_id")

        credential_preview = V20CredPreview.from_dict(d.pop("credential_preview"))

        filter_ = V20CredFilter.from_dict(d.pop("filter"))

        auto_issue = d.pop("auto_issue", UNSET)

        auto_remove = d.pop("auto_remove", UNSET)

        comment = d.pop("comment", UNSET)

        trace = d.pop("trace", UNSET)

        v20_cred_offer_request = cls(
            connection_id=connection_id,
            credential_preview=credential_preview,
            filter_=filter_,
            auto_issue=auto_issue,
            auto_remove=auto_remove,
            comment=comment,
            trace=trace,
        )

        v20_cred_offer_request.additional_properties = d
        return v20_cred_offer_request

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