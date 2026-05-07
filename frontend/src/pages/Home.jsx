import FileUpload from "../components/FileUpload";
import ChatBox from "../components/ChatBox";
import SummaryPanel from "../components/SummaryPanel"

// Home Page
function Home() {
  return (
    <div>
      <h1>Multimedia RAG Application</h1>

      <FileUpload />

      <hr />

      <ChatBox />

      <hr />

      <SummaryPanel />
    </div>
  );
}

export default Home;