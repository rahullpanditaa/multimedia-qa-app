import FileUpload from "../components/FileUpload";
import ChatBox from "../components/ChatBox";
import SummaryPanel from "../components/SummaryPanel";
import TimestampResults from "../components/TimestampResults";


function Home() {

  return (

    <div className="app-container">

      <h1 className="page-title">
        Multimedia RAG Application
      </h1>


      {/* Upload section */}
      <div className="section-card">

        <FileUpload />

      </div>


      {/* Chat section */}
      <div className="section-card">

        <ChatBox />

      </div>


      {/* Summary section */}
      <div className="section-card">

        <SummaryPanel />

      </div>


      {/* Timestamp section */}
      <div className="section-card">

        <TimestampResults />

      </div>

    </div>
  );
}


export default Home;