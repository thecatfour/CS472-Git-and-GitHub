package nl.tudelft.jpacman.level;

import static org.assertj.core.api.Assertions.assertThat;

import nl.tudelft.jpacman.board.Square;
import nl.tudelft.jpacman.board.Unit;
import nl.tudelft.jpacman.npc.Ghost;
import nl.tudelft.jpacman.npc.ghost.GhostFactory;
import nl.tudelft.jpacman.points.DefaultPointCalculator;
import nl.tudelft.jpacman.sprite.EmptySprite;
import nl.tudelft.jpacman.sprite.PacManSprites;
import nl.tudelft.jpacman.sprite.Sprite;

import org.junit.jupiter.api.Test;

// Based on the BasicSquare class
class TestSquare extends Square
{
    /**
     * Creates a new test square.
     */
    TestSquare() {
        super();
    }

    @Override
    public boolean isAccessibleTo(Unit unit) {
        return true;
    }

    @Override
    @SuppressWarnings("return.type.incompatible")
    public Sprite getSprite() {
        return null;
    }
}

public class LesliePlayerCollisionsTest
{
    private static final PacManSprites SPRITES = new PacManSprites();

    private PlayerFactory playerFactory = new PlayerFactory(SPRITES);
    private Player player;

    private GhostFactory ghostFactory = new GhostFactory(SPRITES);
    private Ghost ghost;

    private Pellet pellet = new Pellet(1, new EmptySprite());
    private Square pelletSquare;

    private PlayerCollisions playerCollisions = new PlayerCollisions(new DefaultPointCalculator());

    /*

    Helper methods to set up objects for testing.

     */

    private void resetPlayer()
    {
        player = playerFactory.createPacMan();
    }

    private void resetGhost()
    {
        ghost = ghostFactory.createBlinky();
    }

    private void resetPellet()
    {
        pelletSquare = new TestSquare();
        pellet = new Pellet(1, new EmptySprite());
        pellet.occupy(pelletSquare);
    }

    /**
     * Tests the playerVersusGhost method by checking if it kills the player properly.
     */
    @Test
    public void testPlayerVersusGhost()
    {
        resetPlayer();
        resetGhost();

        playerCollisions.playerVersusGhost(player, ghost);

        assertThat(!player.isAlive() && player.getKiller().equals(ghost)).isEqualTo(true);
    }

    /**
     * Tests the playerVersusPellet method by checking if it adds the pellet's points to the player and removes the pellet.
     */
    @Test
    public void testPlayerVersusPellet()
    {
        resetPlayer();
        resetPellet();

        int beforeScore = player.getScore();

        playerCollisions.playerVersusPellet(player, pellet);

        assertThat(beforeScore < player.getScore() && !pellet.hasSquare()).isEqualTo(true);
    }

    /**
     * Tests the pellet first part of the collide method.
     */
    @Test
    public void testPelletColliding()
    {
        resetPlayer();
        resetPellet();

        // Make sure the pellet/player method works correctly
        int beforeScore = player.getScore();

        playerCollisions.collide(pellet, player);

        assertThat(beforeScore < player.getScore() && !pellet.hasSquare()).isEqualTo(true);

        // Check the else branch
        resetPellet();

        playerCollisions.collide(pellet, null);

        assertThat(pellet.hasSquare()).isEqualTo(true); // Pellet should be unchanged
    }

    /**
     * Tests the ghost first part of the collide method.
     */
    @Test
    public void testGhostColliding()
    {
        resetPlayer();
        resetGhost();

        // Make sure the ghost/player method works correctly
        playerCollisions.collide(ghost, player);

        assertThat(!player.isAlive() && player.getKiller().equals(ghost)).isEqualTo(true);

        // Check the else branch
        resetGhost();

        playerCollisions.collide(ghost, null);
    }

    /**
     * Tests the player first part of the collide method.
     */
    @Test
    public void testPlayerColliding()
    {
        resetPlayer();
        resetGhost();
        resetPellet();

        // Make sure the player/ghost method works correctly
        playerCollisions.collide(player, ghost);

        assertThat(!player.isAlive() && player.getKiller().equals(ghost)).isEqualTo(true);

        // Make sure the player/pellet method works correctly
        resetPlayer();

        int beforeScore = player.getScore();

        playerCollisions.collide(player, pellet);

        assertThat(beforeScore < player.getScore() && !pellet.hasSquare()).isEqualTo(true);

        // Check the else branch
        resetPlayer();

        beforeScore = player.getScore();

        playerCollisions.collide(player, null);

        assertThat(player.isAlive() && player.getScore() == beforeScore).isEqualTo(true); // Player should be unchanged
    }

    /**
     * Tests the else section of the collision method.
     */
    @Test
    public void testCollide()
    {
        resetPlayer();
        resetPellet();

        int beforeScore = player.getScore();

        // Check the else branch as the other tests check the individual branches
        playerCollisions.collide(null, player);
        playerCollisions.collide(null, pellet);

        assertThat(player.isAlive() && player.getScore() == beforeScore && pellet.hasSquare()).isEqualTo(true); // Player and pellet should be unchanged
    }
}
