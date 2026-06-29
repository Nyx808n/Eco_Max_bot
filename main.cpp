#include <iostream>
#include <fstream>
#include <string>
#include <boost/asio.hpp>

#include "HttpServer.h"
#include "Router.h"


namespace net = boost::asio;
using tcp = net::ip::tcp;



int main()
{
	try
	{
		net::io_context io_context;
		// HTTP server
		auto router = std::make_shared<Router>();

		tcp::endpoint endpoint(tcp::v4(), 8080);

		HttpServer server(io_context, endpoint, router);
		
		server.run();

		std::cout << "Server is running on port 8080..." << std::endl;


		//// запуск event loop
		io_context.run();

	}
	catch (const std::exception& e)
	{
		std::cerr << "Error: " << e.what() << std::endl;
	}




	return 0;


}
