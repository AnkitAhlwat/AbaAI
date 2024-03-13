import MoveHistory from "./MoveHistory";
import AIMoveDisplay from "./AiMove";
import GameClock from "./Clock";

const CurrentGameBar = (props) => {
  const { movesStack, aiMove } = props;

  return (
    <>
      <GameClock />
      <AIMoveDisplay aiMove={aiMove} />
      <MoveHistory movesStack={movesStack} />
    </>
  );
};

export default CurrentGameBar;
