import {
	ApolloClient,
	InMemoryCache,
	HttpLink,
	concat,
	ApolloLink,
} from "@apollo/client";
import { Constants } from "../utils";

const httpLink = new HttpLink({
	uri: process.env.NEXT_PUBLIC_BACKEND_URL,
});

const authMiddleware = new ApolloLink((operation, forward) => {
	operation.setContext({
		headers: {
			"Content-Type": "application/json",
			authorization: localStorage.getItem(Constants.ACCESS_TOKEN)
				? `JWT ${localStorage.getItem(Constants.ACCESS_TOKEN)}`
				: null,
		},
	});
	return forward(operation);
});

const client = new ApolloClient({
	link: concat(authMiddleware, httpLink),
	cache: new InMemoryCache(),
});

export default client;
