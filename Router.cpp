#include "Router.h"
#include <iostream>
#include <nlohmann/json.hpp>

Router::Router() {}

std::shared_ptr<Request> Router::route(const std::string& path, std::string& body)
{
    auto request = std::make_shared<Request>();

    std::cout << "=== Router::route ===" << std::endl;
    std::cout << "Path: " << path << std::endl;
    std::cout << "Body: " << body << std::endl;

    if (path == "/webhook/max") {
        try {
            auto json = nlohmann::json::parse(body);

            // Поля, которые приходят от MAX
            std::string userId = json.value("user_id", "");
            std::string userName = json.value("user_name", "");
            std::string text = json.value("text", "");
            std::string photoUrl = json.value("photo_url", "");

            double lat = 0, lon = 0;
            if (json.contains("location") && !json["location"].is_null()) {
                lat = json["location"].value("lat", 0.0);
                lon = json["location"].value("lon", 0.0);
            }

            std::cout << "User: " << userId << ", Name: " << userName << ", Text: " << text << std::endl;

            // Здесь ты можешь вызвать свою бизнес-логику.
            // Например, сохранить пользователя в БД или обработать команду.
            // Пока просто логируем и отвечаем "OK".

            request->setSuccess(true);
            nlohmann::json responseJson;
            responseJson["success"] = true;
            responseJson["message"] = "OK";
            request->responseBody_ = responseJson.dump();

        }
        catch (const std::exception& e) {
            std::cout << "Parse error: " << e.what() << std::endl;
            request->setSuccess(false);
            request->setErrorMessage("Invalid JSON");
            nlohmann::json responseJson;
            responseJson["success"] = false;
            responseJson["message"] = "Invalid JSON";
            request->responseBody_ = responseJson.dump();
        }
    }
    else {
        // Любой другой путь — возвращаем 404 в теле
        request->setSuccess(false);
        request->setErrorMessage("Not found");
        nlohmann::json responseJson;
        responseJson["success"] = false;
        responseJson["message"] = "Not found";
        request->responseBody_ = responseJson.dump();
    }

    return request;
}