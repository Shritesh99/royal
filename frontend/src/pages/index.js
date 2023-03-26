import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { useRecoilState } from "recoil";
import { Constants } from "../utils";
import { LoadingAtom } from "../atoms";

export default function Home() {
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	const router = useRouter();
	useEffect(() => {
		setLoading(true);
		if (!localStorage.getItem(Constants.GOOGLE_CLIENT_TOKEN)) {
			router.replace("/auth");
		}
		setLoading(false);
	}, []);
	return <>Hello World!!</>;
}
