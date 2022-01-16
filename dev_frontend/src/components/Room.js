import React, { Component } from "react";
import { Grid, Button, Typography } from "@material-ui/core";
import Perishable from "./Perishable";

export default class Room extends Component {
	constructor(props) {
		super(props);
		this.state = {
			// votesToSkip: 2,
			// guestCanPause: false,
			// isHost: false,
			// showSettings: false,
			username: "",
			basketLoaded: false,
			basket: false,
		};
		this.code = window.location.href.split("/").slice(-1)[0];
		// this.leaveButtonPressed = this.leaveButtonPressed.bind(this);
		// this.updateShowSettings = this.updateShowSettings.bind(this);
		// this.renderSettingsButton = this.renderSettingsButton.bind(this);
		// this.renderSettings = this.renderSettings.bind(this);
		this.getBasketDetails = this.getBasketDetails.bind(this);
		this.getUsername = this.getUsername.bind(this);
		// this.authenticateSpotify = this.authenticateSpotify.bind(this);
		// this.getCurrentSong = this.getCurrentSong.bind(this);
		this.renderPerishables = this.renderPerishables.bind(this);
		this.getBasketDetails();
		this.getUsername();
		// this.getCurrentSong();
	}

	// componentDidMount() {
	// 	this.interval = setInterval(this.getCurrentSong, 1000);
	// }

	// componentWillUnmount() {
	// 	clearInterval(this.interval);
	// }

	getBasketDetails() {
		return fetch("/api/get_code_perish" + "?code=" + this.code).then(
			(response) => {
				if (response.ok) {
					return response.json().then((data) => {
						console.log("data: ", data);
						this.setState({
							basketLoaded: true,
							basket: data,
						});
					});
				}
			}
		);
	}

	getUsername() {
		return fetch("/api/utilis/retrieve_username")
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				this.setState({
					username: data.username,
				});
			});
	}

	// authenticateSpotify() {
	// 	fetch("/spotify/is-authenticated")
	// 		.then((response) => response.json())
	// 		.then((data) => {
	// 			this.setState({ spotifyAuthenticated: data.status });
	// 			console.log(data.status);
	// 			if (!data.status) {
	// 				fetch("/spotify/get-auth-url")
	// 					.then((response) => response.json())
	// 					.then((data) => {
	// 						window.location.replace(data.url);
	// 					});
	// 			}
	// 		});
	// }

	// getCurrentSong() {
	// 	fetch("/spotify/current-song")
	// 		.then((response) => {
	// 			if (!response.ok) {
	// 				return {};
	// 			} else {
	// 				return response.json();
	// 			}
	// 		})
	// 		.then((data) => {
	// 			this.setState({ song: data });
	// 			console.log(data);
	// 		});
	// }

	leaveButtonPressed() {
		const requestOptions = {
			method: "POST",
			headers: { "Content-Type": "application/json" },
		};
		fetch("/api/leave_room", requestOptions).then((_response) => {
			this.props.leaveRoomCallback();
			this.props.history.push("/frontend");
		});
	}

	updateShowSettings(value) {
		this.setState({
			showSettings: value,
		});
	}

	renderSettings() {
		return (
			<Grid container spacing={1}>
				<Grid item xs={12} align="center">
					<CreateRoomPage
						update={true}
						votesToSkip={this.state.votesToSkip}
						guestCanPause={this.state.guestCanPause}
						roomCode={this.roomCode}
						updateCallback={this.getBasketDetails}
					/>
				</Grid>
				<Grid item xs={12} align="center">
					<Button
						variant="contained"
						color="secondary"
						onClick={() => this.updateShowSettings(false)}>
						Close
					</Button>
				</Grid>
			</Grid>
		);
	}

	renderSettingsButton() {
		return (
			<Grid item xs={12} align="center">
				<Button
					variant="contained"
					color="primary"
					onClick={() => this.updateShowSettings(true)}>
					Settings
				</Button>
			</Grid>
		);
	}

	renderPerishables() {
		let PerishableList = [];
		this.state.basket.forEach((item, index) => {
			console.log(item);
			PerishableList.push(<Perishable {...item} key={index} />);
		});
		return <Grid>{PerishableList}</Grid>;
	}

	render() {
		// Returns Settings only, if show settings is true
		// if (this.state.showSettings) {
		// 	return this.renderSettings();
		// }
		return (
			<Grid container spacing={1}>
				<Grid item xs={12} align="center">
					<Typography variant="h6" component="h6">
						User : {this.state.username}
					</Typography>
				</Grid>
				{this.state.basketLoaded ? this.renderPerishables() : null}
				<Grid item xs={12} align="center">
					<Button
						variant="contained"
						color="primary"
						// onClick={this.leaveButtonPressed}
						href="/frontend/login">
						Logout
					</Button>
				</Grid>
				{/* loaded {this.code} */}
			</Grid>
		);
	}
}
