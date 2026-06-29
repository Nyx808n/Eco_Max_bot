#include "Session.h"
//#include "RequestParser.h"
#include "ResponseBuilder.h"
#include <iostream>

Session::Session(tcp::socket socket, std::shared_ptr<Router> router)
    : socket_(std::move(socket)), router_(router)
{
    std::cout << "Session created" << std::endl;
}

void Session::start()
{
    std::cout << "Session started" << std::endl;
    doRead();
}

void Session::doRead()
{
    auto self = shared_from_this();

    async_read(socket_, buffer_, request_,
        [self](beast::error_code ec, std::size_t bytes_transferred)
        {
            if (ec)
            {
                std::cerr << "Read error: " << ec.message() << std::endl;
                return;
            }
            std::cout << "Received " << bytes_transferred << " bytes" << std::endl;
            self->handleRequest();
        });
}

//void Session::handleRequest()
//{
//    std::cout << "=== Session::handleRequest ===" << std::endl;
//
//    std::string path = request_.target();
//    std::string body = request_.body();
//
//    std::cout << "Path: " << path << std::endl;
//    std::cout << "Body: " << body << std::endl;
//
//    // Всегда возвращаем 200 OK и тело запроса (или стандартный ответ)
//    response_.version(request_.version());
//    response_.set(http::field::content_type, "application/json");
//    response_.result(http::status::ok);
//
//    // Можно вернуть echo или фиксированный json
//    std::string responseBody = "{\"success\":true}";
//    response_.body() = responseBody;
//    response_.prepare_payload();
//    doWrite();
//}
void Session::handleRequest()
{
    std::cout << "=== Session::handleRequest ===" << std::endl;

    std::string path = request_.target();
    std::string body = request_.body();

    std::cout << "Path: " << path << std::endl;
    std::cout << "Body: " << body << std::endl;

    // Отправляем запрос в роутер
    auto request = router_->route(path, body);

    // Формируем ответ
    response_.version(request_.version());
    response_.set(http::field::content_type, "application/json");
    response_.result(http::status::ok);

    if (!request->responseBody_.empty()) {
        response_.body() = request->responseBody_;
    }
    else {
        nlohmann::json json;
        json["success"] = request->success_;
        json["message"] = request->errorMessage_.empty() ? "OK" : request->errorMessage_;
        response_.body() = json.dump();
    }

    response_.prepare_payload();
    doWrite();
}

void Session::doWrite()
{
    auto self = shared_from_this();

    http::async_write(socket_, response_, [self](beast::error_code ec, std::size_t)
        {
            if (ec)
            {
                std::cerr << "Write error: " << ec.message() << std::endl;
                return;
            }
            std::cout << "Response sent" << std::endl;

            if (self->response_.keep_alive())
            {
                self->request_ = {};
                self->response_ = {};
                self->buffer_.consume(self->buffer_.size());
                self->doRead();
            }
            else
            {
                beast::error_code ec_close;
                self->socket_.shutdown(tcp::socket::shutdown_send, ec_close);
            }
        });
}