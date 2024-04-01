using UnityEngine;
using UnityEngine.UI;

public class DisplayScore : MonoBehaviour
{
    public Text scoreText;
    public Quest quest;

    public void FixedUpdate()
    {
        scoreText.text = quest.GetScore().ToString();
    }
}