import { gql } from "@apollo/client";
export default gql`
	query me {
		me {
			picture
			dob
			gender
			ls
			user {
				firstName
				lastName
				email
			}
		}
	}
`;
