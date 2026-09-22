import functions_framework
from google.cloud.devtools import cloudbuild_v1
from google.cloud import storage

@functions_framework.http
def hello_http(request):
    output = []

    # Test 1: Cloud Build permission (should SUCCEED - test-sa has cloudbuild.builds.editor)
    try:
        client = cloudbuild_v1.CloudBuildClient()
        project_id = "my-generic-project-504019"
        request = cloudbuild_v1.ListBuildsRequest(
            project_id=project_id,
            page_size=1,
        )
        builds = client.list_builds(request=request)
        list(builds)
        output.append("Cloud Build call: SUCCESS YAHOO")
    except Exception as e:
        output.append(f"Cloud Build call: FAIL!!!! - {e}")

    # Test 2: Cloud Storage permission (should FAIL - test-sa has no storage role)
    try:
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())
        output.append(f"Storage call: SUCCESS YAHOO - found {len(buckets)} buckets")
    except Exception as e:
        output.append(f"Storage call: FAIL!!!! - {e}!!!!")

    return "\n".join(output)