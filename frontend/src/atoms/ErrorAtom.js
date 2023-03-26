import { atom, selector } from "recoil";

const ErrorAtom = atom({
	key: "Error",
	default: "",
});

const isEmptyErrorSelector = selector({
	key: "isEmptyError",
	get: ({ get }) => {
		if (get(ErrorAtom).length === 0) return false;
		return get(ErrorAtom);
	},
});

export { ErrorAtom, isEmptyErrorSelector };
