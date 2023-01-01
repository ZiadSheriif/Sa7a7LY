// Import themes
import darkTheme from "./Theme/darkTheme";
import defaultTheme from "./Theme/defaultTheme";
import lightTheme from "./Theme/lightTheme";

// Import theme provider from styled components
import { ThemeProvider } from "styled-components";
import "./App.css";
import ImagesAndVideosTab from "./Components/ImagesAndVideosTab/ImagesAndVideosTab";

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={lightTheme}>
        <header className="App-header">
          <ImagesAndVideosTab />
        </header>
      </ThemeProvider>
    </div>
  );
}

export default App;
