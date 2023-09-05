import "@/styles/globals.css";
import "react-toastify/dist/ReactToastify.css";

import { GoogleOAuthProvider } from "@react-oauth/google";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { useRecoilValue, RecoilRoot, useRecoilState } from "recoil";
import { LoadingAtom, ErrorAtom, isLoggedInSelector, AuthAtom } from "../atoms";
import {
	DobGenderModal,
	Layout,
	Loading,
	FSLSMQuestionModal,
	MVModal,
} from "../components";
import { ToastContainer, toast } from "react-toastify";
import { ApolloProvider, useLazyQuery } from "@apollo/client";
import { Client } from "../config";
import { Me } from "../gql";
import { Constants } from "../utils";
import { User } from "../models";

function Application({ Component, pageProps, props }) {
	const router = useRouter();
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	const [err, setErr] = useRecoilState(ErrorAtom);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	const [auth, setAuth] = useRecoilState(AuthAtom);

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
		if (err.length !== 0) {
			toast.error(err);
		}
	});
	if (loading) return <Loading />;
	return (
		<>
			<ToastContainer />
			{isLoggedIn ? (
				<>
					<DobGenderModal />
					<FSLSMQuestionModal />
					<MVModal />
				</>
			) : (
				<></>
			)}
			<div className="hero-body">
				<Component {...pageProps} />
			</div>
		</>
	);
}

export default function App({ Component, pageProps }) {
	return (
		<RecoilRoot>
			<ApolloProvider client={Client}>
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
