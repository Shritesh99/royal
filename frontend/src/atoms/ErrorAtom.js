import { atom, selector } from "recoil";

const ErrorAtom = atom({
	key: "Error",
	default: "",
});

export { ErrorAtom };
