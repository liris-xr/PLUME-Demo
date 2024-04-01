using UnityEngine;

[ExecuteAlways]
public class FollowCamera : MonoBehaviour
{
    public Camera target;
    public Vector3 offsetPosition;

    private void Update()
    {
        var t = transform;
        var targetTransform = target.transform;
        t.position = targetTransform.position + offsetPosition;
        t.rotation = Quaternion.Euler(0, targetTransform.eulerAngles.y, 0);
    }
}