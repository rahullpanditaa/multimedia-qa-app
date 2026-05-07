import FileUpload from "../components/FileUpload";
import ChatBox from "../components/ChatBox";
import SummaryPanel from "../components/SummaryPanel"
import TimestampResults from "../components/TimestampResults";

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

      <hr />

      <TimestampResults />
    </div>
  );
}

export default Home;