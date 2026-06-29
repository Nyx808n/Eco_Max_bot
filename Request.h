#ifndef REQUEST_H
#define REQUEST_H
#include <string>
#include <memory>

// Класс Request представляет собой структуру данных, которая содержит информацию о запросе на регистрацию или аутентификацию пользователя. 
// Он включает в себя поля для хранения логина, электронной почты, пароля, соли, а также флаг успеха и сообщение об ошибке. Кроме того, он может 
// содержать указатель на объект User, который будет заполнен при успешной аутентификации.
class Request
{
public:
	bool success_ = false;
	std::string errorMessage_;
	std::string responseBody_;

	Request()
	{
	}
	
	
	~Request() = default;

	void setSuccess(bool success);
	void setErrorMessage(const std::string& errorMessage);

};

#endif // REQUEST_H

