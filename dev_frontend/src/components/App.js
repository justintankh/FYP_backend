import React, { Component } from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import CreatePage from "./CreatePage";
import HomePage from "./HomePage";
import LoginPage from "./LoginPage";
import Room from "./Room";

export default class App extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="center">
				<Router>
					<Routes>
						<Route exact path="/frontend" element={<HomePage />} />
						<Route
							path="/frontend/signup"
							element={<CreatePage />}
						/>
						<Route path="/frontend/login" element={<LoginPage />} />
						<Route
							path="/frontend/basket/:code"
							element={<Room />}
						/>
					</Routes>
				</Router>
			</div>
		);
	}
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
