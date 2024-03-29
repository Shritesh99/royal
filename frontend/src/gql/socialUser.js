import { gql } from "@apollo/client";
export default gql`
	mutation socialUser($token: String!) {
		socialUser(accessToken: $token, provider: "google-oauth2") {
			token
			refreshToken
			user {
				picture
				dob
				gender
				ls
				motivation
				user {
					firstName
					lastName
					email
				}
			}
		}
	}
`;
