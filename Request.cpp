#include "Request.h"

void Request::setSuccess(bool success)
{
	success_ = success;
	errorMessage_ = "";
}

void Request::setErrorMessage(const std::string& errorMessage)
{
	errorMessage_ = errorMessage;
}
