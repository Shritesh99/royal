import { gql } from "@apollo/client";
export default gql`
	query me {
		me {
			picture
			dob
			gender
			user {
				firstName
				lastName
				email
			}
		}
	}
`;
