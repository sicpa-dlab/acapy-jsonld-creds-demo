from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.attach_decorator import AttachDecorator
from ..models.invitation_receive_request_service import InvitationReceiveRequestService
from ..models.service import Service
from ..types import UNSET, Unset

T = TypeVar("T", bound="InvitationReceiveRequest")


@attr.s(auto_attribs=True)
class InvitationReceiveRequest:
    """ """

    id: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    handshake_protocols: Union[Unset, List[str]] = UNSET
    label: Union[Unset, str] = UNSET
    requestattach: Union[Unset, List[AttachDecorator]] = UNSET
    service: Union[Unset, InvitationReceiveRequestService] = UNSET
    service_blocks: Union[Unset, List[Service]] = UNSET
    service_dids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        handshake_protocols: Union[Unset, List[str]] = UNSET
        if not isinstance(self.handshake_protocols, Unset):
            handshake_protocols = self.handshake_protocols

        label = self.label
        requestattach: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.requestattach, Unset):
            requestattach = []
            for requestattach_item_data in self.requestattach:
                requestattach_item = requestattach_item_data.to_dict()

                requestattach.append(requestattach_item)

        service: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.to_dict()

        service_blocks: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.service_blocks, Unset):
            service_blocks = []
            for service_blocks_item_data in self.service_blocks:
                service_blocks_item = service_blocks_item_data.to_dict()

                service_blocks.append(service_blocks_item)

        service_dids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.service_dids, Unset):
            service_dids = self.service_dids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["@id"] = id
        if type is not UNSET:
            field_dict["@type"] = type
        if handshake_protocols is not UNSET:
            field_dict["handshake_protocols"] = handshake_protocols
        if label is not UNSET:
            field_dict["label"] = label
        if requestattach is not UNSET:
            field_dict["request~attach"] = requestattach
        if service is not UNSET:
            field_dict["service"] = service
        if service_blocks is not UNSET:
            field_dict["service_blocks"] = service_blocks
        if service_dids is not UNSET:
            field_dict["service_dids"] = service_dids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("@id", UNSET)

        type = d.pop("@type", UNSET)

        handshake_protocols = cast(List[str], d.pop("handshake_protocols", UNSET))

        label = d.pop("label", UNSET)

        requestattach = []
        _requestattach = d.pop("request~attach", UNSET)
        for requestattach_item_data in _requestattach or []:
            requestattach_item = AttachDecorator.from_dict(requestattach_item_data)

            requestattach.append(requestattach_item)

        _service = d.pop("service", UNSET)
        service: Union[Unset, InvitationReceiveRequestService]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = InvitationReceiveRequestService.from_dict(_service)

        service_blocks = []
        _service_blocks = d.pop("service_blocks", UNSET)
        for service_blocks_item_data in _service_blocks or []:
            service_blocks_item = Service.from_dict(service_blocks_item_data)

            service_blocks.append(service_blocks_item)

        service_dids = cast(List[str], d.pop("service_dids", UNSET))

        invitation_receive_request = cls(
            id=id,
            type=type,
            handshake_protocols=handshake_protocols,
            label=label,
            requestattach=requestattach,
            service=service,
            service_blocks=service_blocks,
            service_dids=service_dids,
        )

        invitation_receive_request.additional_properties = d
        return invitation_receive_request

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
