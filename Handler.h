#pragma once

#include <memory>
#include "Request.h"

// Класс Handler содержит указатель на следующий обработчик в цепочке и определяет интерфейс для обработки запроса.
// Он имеет метод setNext для установки следующего обработчика и виртуальный метод handle, который обрабатывает запрос и передает его следующему обработчику, если он существует.
class Handler
{
protected:
	std::shared_ptr<Handler>next_;

public:
	Handler() = default;
	virtual ~Handler() = default;

	void setNext(std::shared_ptr<Handler> next)
	{
		next_ = next;
	}
	virtual void handle(Request& request)
	{
		if (next_)
		{
			next_->handle(request);
		}
	}

};
