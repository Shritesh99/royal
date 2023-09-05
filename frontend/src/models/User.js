export class User {
	constructor(data) {
		this.firstName = data.user.firstName;
		this.lastName = data.user.lastName;
		this.email = data.user.email;
		this.dob = data.dob;
		this.gender = data.gender;
		this.picture = data.picture;
		this.ls = data.ls;
		this.motivation = data.motivation;
	}
}
