using System;
using System.Collections.Generic;
using System.Linq;
using PLUME.Core.Recorder;
using UnityEngine;
using UnityEngine.UI;

public class Quest : MonoBehaviour
{
    public PlayerManager playerManager;

    [Header("Quest Description")] public string title;
    public string description;

    [Header("Canvas Parameters")] public Text titleText;
    public Text descriptionText;
    public Text secondaryText;

    [Header("Timer")] public Text timerText;
    public float timeRemaining = 300;
    public bool timerIsRunning;

    public GameObject lobbyWall;

    private List<EasterEgg> _remainingEggs = new();
    private int _maxNumberOfEggs;

    public AudioSource audioSource;
    public AudioClip eggPickUpSound;
    public AudioClip startSound;
    public AudioClip endSound;
    public AudioClip countdownSound;
    private bool _countdownStartedPlaying;

    private void Start()
    {
        _remainingEggs = FindObjectsOfType<EasterEgg>().ToList();
        _maxNumberOfEggs = _remainingEggs.Count;

        titleText.text = title;
        descriptionText.text = description;
        secondaryText.text = "";

        playerManager.MovePlayerToLobby(false);
    }

    private void Update()
    {
        if (!timerIsRunning)
            return;

        if (timeRemaining > 0)
        {
            timeRemaining -= Time.deltaTime;
            timerText.text = TimeSpan.FromSeconds(timeRemaining).ToString(@"mm\:ss");
        }

        if (timeRemaining <= 0 || _remainingEggs.Count == 0)
        {
            OnQuestEnd();
            timeRemaining = 0;
            timerIsRunning = false;
        }
        else if (timeRemaining <= 8 && !_countdownStartedPlaying)
        {
            audioSource.PlayOneShot(countdownSound);
            _countdownStartedPlaying = true;
        }
    }

    public void OnQuestBegin()
    {
        if (timerIsRunning)
            return;

        timerIsRunning = true;
        lobbyWall.SetActive(false);
        audioSource.PlayOneShot(startSound);
    }

    public void OnQuestEnd()
    {
        if (PlumeRecorder.IsRecording)
        {
            PlumeRecorder.RecordMarker($"Score: {GetScore()}/{_maxNumberOfEggs}");
        }

        lobbyWall.SetActive(true);
        titleText.text = "Congratulations!";
        descriptionText.text = "Final score";
        secondaryText.text = "Come back to the real world!";
        audioSource.PlayOneShot(endSound);

        playerManager.MovePlayerToLobby(true);
        playerManager.StopApplication();
    }

    public int GetScore()
    {
        return _maxNumberOfEggs - _remainingEggs.Count;
    }

    public void OnEggPickUp(EasterEgg obj)
    {
        if (!_remainingEggs.Contains(obj))
            return;

        _remainingEggs.Remove(obj);
        audioSource.PlayOneShot(eggPickUpSound);
        Destroy(obj.gameObject);
    }
}