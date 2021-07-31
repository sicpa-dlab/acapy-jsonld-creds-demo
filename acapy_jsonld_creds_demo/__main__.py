"""Run the demo."""

from datetime import date
import json
import os
import time

from acapy_client import Client
from acapy_client.api.connection import create_invitation, receive_invitation
from acapy_client.api.credentials import post_credentials_w3c
from acapy_client.api.issue_credential_v20 import (
    issue_credential_automated as issue_credential_v20_automated,
)
from acapy_client.api.wallet import create_did
from acapy_client.models import (
    CreateInvitationRequest,
    ReceiveInvitationRequest,
    V20CredSendRequest,
)
from acapy_client.models.did_create import DIDCreate
from acapy_client.models.did_create_method import DIDCreateMethod
from acapy_client.models.ld_proof_vc_detail import LDProofVCDetail
from acapy_client.models.v20_cred_filter import V20CredFilter
from acapy_client.models.w3c_credentials_list_request import W3CCredentialsListRequest


HOLDER_URL = os.environ.get("HOLDER", "http://localhost:3001")
ISSUER_URL = os.environ.get("ISSUER", "http://localhost:3003")


def describe(description: str, api):
    def _describe(**kwargs):
        print(description)
        request = api._get_kwargs(**kwargs)
        print("Request:", json.dumps(request, indent=2))
        result = api.sync_detailed(**kwargs)
        if not result.parsed:
            raise Exception("Request failed: {}".format(repr(result)))
        print("Response:", json.dumps(result.parsed.to_dict(), indent=2))
        return result.parsed

    return _describe


def main():
    """Run steps."""
    holder = Client(base_url=HOLDER_URL)
    issuer = Client(base_url=ISSUER_URL)

    # Establish Connection {{{
    holder_conn_record = describe("Create new invitation in holder", create_invitation)(
        client=holder, json_body=CreateInvitationRequest(), auto_accept="true"
    )

    issuer_conn_record = describe("Receive invitation in issuer", receive_invitation)(
        client=issuer,
        json_body=ReceiveInvitationRequest.from_dict(
            holder_conn_record.invitation.to_dict()
        ),
    )
    # }}}

    # Prepare signing DID {{{
    did_info = describe(
        "Create new DID for publishing to ledger in issuer", create_did
    )(client=issuer, json_body=DIDCreate(method=DIDCreateMethod.KEY)).result
    # }}}

    print("Pausing to allow connection to finish...")
    time.sleep(1)

    # Issue Credential v2 {{{
    describe("Issue Credential v2 to holder", issue_credential_v20_automated)(
        client=issuer,
        json_body=V20CredSendRequest(
            connection_id=issuer_conn_record.connection_id,
            auto_remove=False,
            comment="nothing",
            filter_=V20CredFilter(
                ld_proof=LDProofVCDetail.from_dict(
                    {
                        "credential": {
                            "@context": [
                                "https://www.w3.org/2018/credentials/v1",
                                "https://www.w3.org/2018/credentials/examples/v1",
                            ],
                            "type": [
                                "VerifiableCredential",
                                "UniversityDegreeCredential",
                            ],
                            "issuer": did_info.did,
                            "issuanceDate": str(date.today()),
                            "credentialSubject": {
                                "degree": {
                                    "type": "BachelorDegree",
                                    "name": "Bachelor of Science and Arts",
                                }
                            },
                        },
                        "options": {"proofType": "Ed25519Signature2018"},
                    }
                )
            ),
        ),
    )
    # }}}

    print("Pausing to allow credential exchange to occur...")
    time.sleep(2)
    describe("Holder retrieve credentials", post_credentials_w3c)(
        client=holder, json_body=W3CCredentialsListRequest()
    )


if __name__ == "__main__":
    main()
