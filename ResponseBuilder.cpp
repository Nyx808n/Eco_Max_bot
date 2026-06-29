#include "ResponseBuilder.h"

std::string ResponseBuilder::buildResponse(const Request& request)
{
	if (!request.responseBody_.empty())
	{

		return request.responseBody_;
	}

	nlohmann::json json;

	json["success"] = request.success_;

	return json.dump();
}
