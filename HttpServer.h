#ifndef HTTPSERVER_H
#define HTTPSERVER_H



#include <memory>
#include <boost/asio.hpp>

#include "Router.h"

namespace net = boost::asio;
using tcp = net::ip::tcp;



class HttpServer
{
public:
    HttpServer(net::io_context& io_context, tcp::endpoint endpoint,std::shared_ptr<Router>router);
    void run();

private:

	void doAccept();

    tcp::acceptor acceptor_;
	tcp::socket socket_;
    std::shared_ptr<Router> router_;
};

#endif // !HTTPSERVER_H
