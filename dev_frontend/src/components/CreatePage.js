import React, { Component } from "react";
import { Button, Grid, Typography, TextField } from "@material-ui/core";
import { Navigate } from "react-router-dom";

export default class CreatePage extends Component {
	constructor(props) {
		super(props);
		this.state = {
			username: "",
			error: "",
		};
		this._handleTextFieldChange = this._handleTextFieldChange.bind(this);
		this._createButtonPressed = this._createButtonPressed.bind(this);
	}

	_handleTextFieldChange(e) {
		this.setState({
			username: e.target.value,
		});
	}

	_createButtonPressed() {
		console.log(this.state.username);
		const requestOptions = {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				username: this.state.username,
			}),
		};
		fetch("/api/signup", requestOptions)
			.then((response) => {
				response.json().then((data) => {
					if (response.ok) {
						console.log("response ok");
						location.href = `basket/${data.code}`;
					} else {
						console.log("response !ok");
						this.setState({ error: data["Bad request"] });
					}
				});
			})
			.catch((error) => {
				console.log(error);
			});
	}

	render() {
		return (
			<Grid container spacing={1}>
				<Grid item xs={12} align="center">
					<Typography variant="h4" component="h4">
						Enter a Username
					</Typography>
				</Grid>
				{/* Input field */}
				<Grid item xs={12} align="center">
					<TextField
						error={this.state.error ? true : false}
						label="Username"
						placeholder="Enter a Username"
						value={this.state.username}
						helperText={this.state.error}
						variant="outlined"
						onChange={this._handleTextFieldChange}
					/>
				</Grid>
				{/* Buttons */}
				<Grid item xs={12} align="center">
					<Button
						variant="contained"
						color="primary"
						onClick={this._createButtonPressed}>
						Create
					</Button>
				</Grid>
				<Grid item xs={12} align="center">
					<Button
						variant="contained"
						color="secondary"
						href="/frontend">
						Back
					</Button>
				</Grid>
			</Grid>
		);
	}
}
