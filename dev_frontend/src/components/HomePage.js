import React, { Component } from "react";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";

export default class HomePage extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	render() {
		return (
			<Grid container spacing={3}>
				<Grid item xs={12} align="center">
					<Typography variant="h3" compact="h3">
						Grocery tracker
					</Typography>
				</Grid>
				<Grid item xs={12} align="center">
					<ButtonGroup
						disableElevation
						variant="contained"
						color="primary">
						<Button color="secondary" href="/frontend/login">
							Login
						</Button>
						<Button color="primary" href="/frontend/signup">
							Sign Up
						</Button>
					</ButtonGroup>
				</Grid>
			</Grid>
		);
	}
}
