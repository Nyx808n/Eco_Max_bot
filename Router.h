#ifndef ROUTER_H
#define ROUTER_H
#include <memory>
#include <string>
#include "Request.h"


#include <nlohmann/json.hpp>
class Router {
public:
	Router();

	std::shared_ptr<Request> route(const std::string &path,
		std::string& body);



private:
	
};





#endif // !ROUTER_H
