import { atom } from "recoil";

const LoadingAtom = atom({
	key: "Loading",
	default: true,
});

export default LoadingAtom;
