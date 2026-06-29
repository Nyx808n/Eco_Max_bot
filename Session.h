#ifndef SESSION_H
#define SESSION_H

#include <memory>
#include <boost/beast/http.hpp>
#include <boost/beast.hpp>
#include <boost/asio.hpp>
#include "Router.h"

namespace beast = boost::beast;         // from <boost/beast.hpp>
namespace http = beast::http;           // from <boost/beast/http.hpp>
namespace net = boost::asio;            // from <boost/asio.hpp>
using tcp = boost::asio::ip::tcp;       // from <boost/asio/ip/tcp.hpp>

class Session : public std::enable_shared_from_this<Session>
{
public:
	Session(tcp::socket socket, std::shared_ptr<Router> router);
	void start();


private:
	void doRead();
	void handleRequest();
	void doWrite();

	beast::flat_buffer buffer_;
	http::request<http::string_body> request_;
	http::response<http::string_body> response_;
	tcp::socket socket_;
	std::shared_ptr<Router> router_;
};

#endif // !SESSION_H
