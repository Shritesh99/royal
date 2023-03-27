import { useRecoilState, useRecoilValue } from "recoil";
import { useRouter } from "next/router";
import { ErrorAtom, LoadingAtom, AuthAtom, isLoggedInSelector } from "../atoms";

export default function Home() {
	const router = useRouter();

	return <>Hello World!!</>;
}
