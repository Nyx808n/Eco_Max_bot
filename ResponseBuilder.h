#ifndef RESPONSEBUILDER_H
#define RESPONSEBUILDER_H

#include<string>
#include <nlohmann/json.hpp>
#include "Request.h"

class ResponseBuilder
{
public:
	static std::string buildResponse(const Request& request);

};




#endif // !RESPONSEBUILDER_H

