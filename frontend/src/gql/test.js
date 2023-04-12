import { gql } from "@apollo/client";

export default gql`
	query Test($testId: String) {
		test(testId: $testId) {
			success
			testId
			questions {
				id
				text
				choices {
					id
					text
				}
			}
		}
	}
`;
