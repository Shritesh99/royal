import "@/styles/globals.css";
import "react-toastify/dist/ReactToastify.css";

import { GoogleOAuthProvider } from "@react-oauth/google";
import { useEffect, useState } from "react";
import { useRecoilValue, RecoilRoot, useRecoilState } from "recoil";
import {
	LoadingAtom,
	isEmptyErrorSelector,
	isLoggedInSelector,
	AuthAtom,
} from "../atoms";
import { Layout, Loading } from "../components";
import { ToastContainer, toast } from "react-toastify";
import { useRouter } from "next/router";
import { Constants } from "../utils";

const Application = ({ Component, pageProps }) => {
	const router = useRouter();
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	const [auth, setAuth] = useRecoilState(AuthAtom);
	const err = useRecoilValue(isEmptyErrorSelector);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);

	useEffect(() => {
		if (!localStorage.getItem(Constants.ACCESS_TOKEN)) {
			setAuth(null);
			router.replace("/auth");
		} else {
			setAuth(localStorage.getItem(Constants.ACCESS_TOKEN));
		}
		setLoading(false);
	}, []);

	useEffect(() => {
		if (!isLoggedIn) router.replace("/auth");
	});

	useEffect(() => {
		if (err) {
			toast.error(err);
		}
	});
	if (loading) return <Loading />;
	return (
		<>
			<ToastContainer />
			<div className="hero-body container">
				<Component {...pageProps} />
			</div>
		</>
	);
};

export default function App({ Component, pageProps }) {
	return (
		<RecoilRoot>
			<GoogleOAuthProvider
				clientId={process.env.NEXT_PUBLIC_GOOGLE_OAUTH_CLIENT_ID}>
				<Layout>
					<Application
						Component={Component}
						pageProps={pageProps}
					/>
				</Layout>
			</GoogleOAuthProvider>
		</RecoilRoot>
	);
}
