import { atom, selector } from "recoil";

const AuthAtom = atom({
	key: "Auth",
	default: null,
});

const isLoggedInSelector = selector({
	key: "isLoggedIn",
	get: ({ get }) => get(AuthAtom) !== null,
});

export { AuthAtom, isLoggedInSelector };
