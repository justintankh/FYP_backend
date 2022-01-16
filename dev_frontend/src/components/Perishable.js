import React, { Component } from "react";
import {
	Grid,
	Typography,
	Card,
	IconButton,
	LinearProgress,
} from "@material-ui/core";

import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import PauseIcon from "@material-ui/icons/Pause";
import SkipNextIcon from "@material-ui/icons/SkipNext";

export default class Perishable extends Component {
	constructor(props) {
		super(props);
	}

	skipSong() {
		const requestOptions = {
			method: "POST",
			headers: { "Content-Type": "application/json" },
		};
		fetch("/spotify/skip", requestOptions);
	}

	pauseSong() {
		const requestOptions = {
			method: "PUT",
			headers: { "Content-Type": "application/json" },
		};
		fetch("/spotify/pause", requestOptions);
	}

	playSong() {
		const requestOptions = {
			method: "PUT",
			headers: { "Content-Type": "application/json" },
		};
		fetch("/spotify/play", requestOptions);
	}

	render() {
		const register_date = new Date(this.props.rtr_date);
		const expiry_date = new Date(this.props.exp);
		let current_date = new Date();
		const diffDays = Math.ceil(
			Math.abs(expiry_date - register_date) / (1000 * 60 * 60 * 24)
		);
		const passedDays = Math.ceil(
			Math.abs(current_date - register_date) / (1000 * 60 * 60 * 24)
		);
		const leftDays = Math.ceil(
			(expiry_date - current_date) / (1000 * 60 * 60 * 24)
		);

		const expiryProgress = (passedDays / diffDays) * 100;

		return (
			<Card>
				<Grid container alignItems="center">
					<Grid item align="center" xs={4}>
						<img
							src={this.props.img_url}
							height="100%"
							width="100%"
						/>
					</Grid>
					<Grid item align="center" xs={8}>
						<Typography component="h5" variant="h5">
							{this.props.title}
						</Typography>
						<Typography component="h5" variant="subtitle1">
							EXP: {this.props.exp}
						</Typography>
						<Typography
							color={
								expiryProgress > 70
									? "secondary"
									: expiryProgress > 40
									? "primary"
									: "primary"
							}
							variant="inherit">
							Expirying in: {leftDays} Day
						</Typography>
						{/* <div>
							<IconButton
								onClick={() => {
									this.props.is_playing
										? this.pauseSong()
										: this.playSong();
								}}>
								{this.props.is_playing ? (
									<PauseIcon />
								) : (
									<PlayArrowIcon />
								)}
							</IconButton>
							<IconButton onClick={() => this.skipSong()}>
								{this.props.votes} / {this.props.votes_required}
								<SkipNextIcon />
							</IconButton>
						</div> */}
					</Grid>
				</Grid>
				<LinearProgress
					variant="determinate"
					value={expiryProgress}
					color={
						expiryProgress > 70
							? "secondary"
							: expiryProgress > 40
							? "primary"
							: "primary"
					}
				/>
			</Card>
		);
	}
}
