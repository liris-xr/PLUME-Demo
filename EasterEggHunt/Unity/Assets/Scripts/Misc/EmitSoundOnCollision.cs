using System.Collections.Generic;
using UnityEngine;

public class EmitSoundOnCollision : MonoBehaviour
{
    public List<AudioClip> listClips;
    public AudioSource audioSource;

    private void Start()
    {
        audioSource.playOnAwake = false;
        audioSource.loop = false;
    }

    public void OnCollisionEnter(Collision collision)
    {
        if ((collision.collider.CompareTag("wall") || collision.collider.CompareTag("floor")) &&
            !audioSource.isPlaying &&
            collision.relativeVelocity.magnitude > 1)
        {
            audioSource.transform.position = collision.GetContact(0).point;
            var chosenClip = listClips[Random.Range(0, listClips.Count)];
            audioSource.clip = chosenClip;
            audioSource.pitch = 1f + Random.Range(0f, 1f) - 0.5f;
            audioSource.volume =
                0.4f + Mathf.Lerp(0f, 0.6f, Mathf.InverseLerp(1, 8, collision.relativeVelocity.magnitude));
            audioSource.Play();
        }
    }
}