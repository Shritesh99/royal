import { gql } from "@apollo/client";
export default gql`
	mutation addFslsmquestionsResponse($res: [FSLSMQuestionInput]!) {
		addFslsmquestionsResponse(response: $res) {
			success
		}
	}
`;
