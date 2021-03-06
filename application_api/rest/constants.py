from rentomatic.responses import ResponseTypes

STATUS_CODES = dict(
    HTTP_200_OK=200,
    HTTP_400_BAD_REQUEST=400,
    HTTP_404_NOT_FOUND=404,
    HTTP_500_INTERNAL_SERVER_ERROR=500,
)

RESPONSE_STATUS_CODES = {
    ResponseTypes.SUCCESS: STATUS_CODES["HTTP_200_OK"],
    ResponseTypes.PARAMETERS_ERROR: STATUS_CODES["HTTP_400_BAD_REQUEST"],
    ResponseTypes.RESOURCE_ERROR: STATUS_CODES["HTTP_404_NOT_FOUND"],
    ResponseTypes.SYSTEM_ERROR: STATUS_CODES["HTTP_500_INTERNAL_SERVER_ERROR"],
}
