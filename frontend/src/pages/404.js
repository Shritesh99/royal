import Image from "next/image";
import img from "../../public/images/404.jpg";

export default function Custom404() {
	return <Image src={img} alt="img" />;
}
