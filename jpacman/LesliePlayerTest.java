package nl.tudelft.jpacman.level;

import static org.assertj.core.api.Assertions.assertThat;

import nl.tudelft.jpacman.sprite.PacManSprites;
import org.junit.jupiter.api.Test;

public class LesliePlayerTest
{
    private PlayerFactory pf = new PlayerFactory(new PacManSprites());
    private Player p;

    /*

    Test that player.isAlive() works correctly for both
    true and false.

     */
    @Test
    public void testPlayerIsAlive()
    {
        p = pf.createPacMan();

        assertThat(p.isAlive()).isEqualTo(true);
        p.setAlive(false);
        assertThat(p.isAlive()).isEqualTo(false);
    }
}
