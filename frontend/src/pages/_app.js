import "@/styles/globals.css";
import "react-toastify/dist/ReactToastify.css";

import { GoogleOAuthProvider } from "@react-oauth/google";
import { useEffect, useState } from "react";
import { useRecoilValue, RecoilRoot, useRecoilState } from "recoil";
import {
	LoadingAtom,
	isEmptyErrorSelector,
	ErrorAtom,
	isLoggedInSelector,
	AuthAtom,
	DobGenderModalAtom,
} from "../atoms";
import { DobGenderModal, Layout, Loading } from "../components";
import { ToastContainer, toast } from "react-toastify";
import {
	ApolloClient,
	InMemoryCache,
	ApolloProvider,
	HttpLink,
	concat,
	ApolloLink,
	useLazyQuery,
} from "@apollo/client";
import { useRouter } from "next/router";
import { Constants } from "../utils";
import { Me } from "../gql";
import { User } from "../models";

const Application = ({ Component, pageProps }) => {
	const router = useRouter();
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	const [auth, setAuth] = useRecoilState(AuthAtom);
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [dobGenderModalActtive, setDobGenderModal] =
		useRecoilState(DobGenderModalAtom);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);

	const [getMe] = useLazyQuery(Me, {
		onCompleted: (data) => {
			const user = new User(data.me);
			setAuth(user);
			setLoading(false);
		},
		onError: (error) => {
			setErr(error);
			setLoading(false);
		},
	});

	useEffect(() => {
		if (!localStorage.getItem(Constants.ACCESS_TOKEN)) {
			setAuth(null);
			setLoading(false);
			router.replace("/auth");
		} else {
			getMe();
		}
	}, []);

	useEffect(() => {
		if (!isLoggedIn) router.replace("/auth");
		else {
			if (!auth.dob || !auth.gender) {
				setDobGenderModal(true);
			}
		}
	}, [isLoggedIn]);

	useEffect(() => {
		if (err.length !== 0) {
			toast.error(err);
		}
	});
	if (loading) return <Loading />;
	return (
		<>
			<ToastContainer />
			<DobGenderModal />
			<div className="hero-body container">
				<Component {...pageProps} />
			</div>
		</>
	);
};

export default function App({ Component, pageProps }) {
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
	return (
		<RecoilRoot>
			<ApolloProvider client={client}>
				<GoogleOAuthProvider
					clientId={
						process.env.NEXT_PUBLIC_GOOGLE_OAUTH_CLIENT_ID
					}>
					<Layout>
						<Application
							Component={Component}
							pageProps={pageProps}
						/>
					</Layout>
				</GoogleOAuthProvider>
			</ApolloProvider>
		</RecoilRoot>
	);
}
